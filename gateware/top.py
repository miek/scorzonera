#!/usr/bin/env python3

import os
import sys
import logging
import time

import usb1

from amaranth                        import *
from amaranth.build                  import Attrs, DiffPairs, Pins, Resource
from amaranth.lib.cdc                import PulseSynchronizer
from amaranth.lib.fifo               import AsyncFIFO
from usb_protocol.types              import USBRequestType
from usb_protocol.emitters           import DeviceDescriptorCollection

from luna                            import top_level_cli
from luna.usb2                       import *
from luna.gateware.usb.usb2.request  import USBRequestHandler

from luna.gateware.utils.cdc         import synchronize
from luna.gateware.usb.devices.ila   import USBIntegratedLogicAnalyzer
from luna.gateware.usb.devices.ila   import USBIntegratedLogicAnalyzerFrontend

from acm import USBSerialInterface
from cdr import CDR, SymbolSynchroniser
import taxi
from taxi import TaxiDecoder
from uart import UARTRx, UARTTx

VENDOR_ID  = 0x16d0
PRODUCT_ID = 0x0f3b

BULK_ENDPOINT_NUMBER = 1
MAX_BULK_PACKET_SIZE = 64 if os.getenv('LUNA_FULL_ONLY') else 512


class ScorzoneraDevice(Elaboratable):
    """ Simple device that sends data to the host as fast as hardware can.

    This is paired with the python code below to evaluate LUNA throughput.
    """

    def __init__(self):
        pass

    def emit_analysis_vcd(self, filename='-'):
        frontend = USBIntegratedLogicAnalyzerFrontend(ila=self.ila)
        #frontend.emit_vcd(filename)
        frontend.interactive_display()

    def create_descriptors(self):
        """ Create the descriptors we want to use for our device. """

        descriptors = DeviceDescriptorCollection()

        #
        # We'll add the major components of the descriptors we we want.
        # The collection we build here will be necessary to create a standard endpoint.
        #

        # We'll need a device descriptor...
        with descriptors.DeviceDescriptor() as d:
            d.idVendor           = VENDOR_ID
            d.idProduct          = PRODUCT_ID

            d.iManufacturer      = "Mike Walters"
            d.iProduct           = "Scorzonera"
            d.iSerialNumber      = "no serial"

            d.bNumConfigurations = 1


        # ... and a description of the USB configuration we'll provide.
        with descriptors.ConfigurationDescriptor() as c:

            self._serial.add_descriptors(c)

            with c.InterfaceDescriptor() as i:
                i.bInterfaceNumber = 2

                with i.EndpointDescriptor() as e:
                    e.bEndpointAddress = 0x80 | BULK_ENDPOINT_NUMBER
                    e.wMaxPacketSize   = MAX_BULK_PACKET_SIZE


        return descriptors


    def elaborate(self, platform):
        m = Module()

        # Generate our domain clocks/resets.
        m.submodules.car = platform.clock_domain_generator()

        # Create our USB device interface...
        ulpi = platform.request("host_phy")
        m.submodules.usb = usb = USBDevice(bus=ulpi)

        # Create & add ACM serial interface
        self._serial = serial = USBSerialInterface(max_packet_size=MAX_BULK_PACKET_SIZE)
        serial.add_endpoints(usb)
        m.submodules.serial = serial

        # Add our standard control endpoint to the device.
        descriptors = self.create_descriptors()
        control_ep = usb.add_standard_control_endpoint(descriptors)
        serial.add_handlers(control_ep)

        # Add a stream endpoint to our device.
        stream_ep = USBMultibyteStreamInEndpoint(
            byte_width=2,
            endpoint_number=BULK_ENDPOINT_NUMBER,
            max_packet_size=MAX_BULK_PACKET_SIZE
        )
        usb.add_endpoint(stream_ep)

        # Connect our device as a high speed device by default.
        m.d.comb += [
            usb.connect          .eq(1),
            usb.full_speed_only  .eq(1 if os.getenv('LUNA_FULL_ONLY') else 0),

        ]


        platform.add_resources([
            Resource("uart_rx", 0, Pins("7", conn=("pmod", 1))),
            Resource("uart_tx", 0, Pins("8", conn=("pmod", 1))),
        ])
        uart_rx_pin = platform.request("uart_rx", 0, dir="i")
        uart_tx_pin = platform.request("uart_tx", 0, dir="o")
        m.submodules.uart_rx = uart_rx = DomainRenamer("usb")(UARTRx())
        m.submodules.uart_tx = uart_tx = DomainRenamer("usb")(UARTTx())
        m.d.comb += [
            serial.tx.stream_eq(uart_rx.rx),
            uart_rx.rx_pin.eq(uart_rx_pin),

            uart_tx.tx.stream_eq(serial.rx),
            uart_tx_pin.eq(uart_tx.tx_pin),
        ]

        # Primary clock (ECLK / 2)
        sclk = Signal()

        # Fast edge clock
        eclk = Signal()

        pll_lock = Signal()

        m.domains.video = ClockDomain()
        m.d.comb += [
            ClockSignal("video").eq(sclk),
            ResetSignal("video").eq(~pll_lock),
        ]

        platform.add_resources([
            Resource("rx", 0,
                DiffPairs("9", "10", conn=("pmod", 1)),
                Attrs(IO_TYPE="LVDS"))
        ])
        rx = platform.request("rx", 0, dir="i")
        data_4x = Signal(4)

        m.submodules += [
            Instance("CLKDIVF",
                i_CLKI=eclk,
                i_RST=ResetSignal("video"),
                i_ALIGNWD=0,
                o_CDIVX=sclk,
            ),
            Instance("IDDRX2F",
                i_D=rx,
                i_ECLK=eclk,
                i_SCLK=sclk,
                i_RST=ResetSignal("video"),
                o_Q0=data_4x[0],
                o_Q1=data_4x[1],
                o_Q2=data_4x[2],
                o_Q3=data_4x[3],
            ),
            Instance("EHXPLLL",

                # Clock in.
                i_CLKI=m.submodules.car.clkin,
                #i_CLKI=ClockSignal(),

                # Generated clock outputs.
                o_CLKOP=eclk,

                # Status.
                o_LOCK=pll_lock,

                # PLL parameters...
                p_PLLRST_ENA="DISABLED",
                p_INTFB_WAKE="DISABLED",
                p_STDBY_ENABLE="DISABLED",
                p_DPHASE_SOURCE="DISABLED",
                p_CLKOS3_FPHASE=0,
                p_CLKOS3_CPHASE=0,
                p_CLKOS2_FPHASE=0,
                p_CLKOS2_CPHASE=7,
                p_CLKOS_FPHASE=0,
                p_CLKOS_CPHASE=3,
                p_CLKOP_FPHASE=0,
                p_CLKOP_CPHASE=1,
                p_PLL_LOCK_MODE=0,
                p_CLKOS_TRIM_DELAY="0",
                p_CLKOS_TRIM_POL="FALLING",
                p_CLKOP_TRIM_DELAY="0",
                p_CLKOP_TRIM_POL="FALLING",
                p_OUTDIVIDER_MUXD="DIVD",
                p_CLKOS3_ENABLE="DISABLED",
                p_OUTDIVIDER_MUXC="DIVC",
                p_CLKOS2_ENABLE="DISABLED",
                p_OUTDIVIDER_MUXB="DIVB",
                p_CLKOS_ENABLE="DISABLED",
                p_OUTDIVIDER_MUXA="DIVA",
                p_CLKOP_ENABLE="ENABLED",
                p_CLKOS3_DIV=2,
                p_CLKOS2_DIV=2,
                p_CLKOS_DIV=4,
                p_CLKOP_DIV=2,
                p_CLKFB_DIV=16,
                p_CLKI_DIV=3,
                p_FEEDBK_PATH="CLKOP",

                # Internal feedback.
                i_CLKFB=eclk,

                # Control signals.
                i_RST=0,
                i_PHASESEL0=0,
                i_PHASESEL1=0,
                i_PHASEDIR=0,
                i_PHASESTEP=0,
                i_PHASELOADREG=0,
                i_STDBY=0,
                i_PLLWAKESYNC=0,

                # Output Enables.
                i_ENCLKOP=1,
                i_ENCLKOS=1,
                i_ENCLKOS2=0,
                i_ENCLKOS3=0,

                # Synthesis attributes.
                a_FREQUENCY_PIN_CLKI="100.000000",
                a_ICP_CURRENT="9",
                a_LPF_RESISTOR="8"
            ),

        ]

        cdr = CDR()
        m.d.comb += cdr.input.eq(data_4x)
        m.submodules += DomainRenamer("video")(cdr)

        symbol_sync = SymbolSynchroniser(sync_symbol=Const(taxi.SYNC, 10))
        symbol_sync = DomainRenamer("video")(symbol_sync)
        m.submodules += symbol_sync

        taxi_decoder = TaxiDecoder()
        m.submodules += DomainRenamer("video")(taxi_decoder)

        # NRZI decode
        previous_sample = Signal()

        with m.Switch(cdr.data_valid):
            with m.Case(0b11):
                m.d.video += [
                    symbol_sync.input[1].eq(previous_sample ^ cdr.data[1]),
                    symbol_sync.input[0].eq(cdr.data[1]     ^ cdr.data[0]),
                    previous_sample     .eq(cdr.data[0]),
                ]

            with m.Case(0b1):
                m.d.video += [
                    symbol_sync.input[0].eq(previous_sample ^ cdr.data[0]),
                    previous_sample     .eq(cdr.data[0]),
                ]

        m.d.video += symbol_sync.input_valid.eq(cdr.data_valid)

        # Connect SymbolSynchroniser to TaxiDecoder
        m.d.comb += [
            taxi_decoder.symbol        .eq(symbol_sync.symbol),
            taxi_decoder.symbol_valid  .eq(symbol_sync.symbol_valid),
            symbol_sync.resync         .eq(taxi_decoder.violation),
        ]

        # Create a FIFO to bridge from the video -> usb domain
        fifo = AsyncFIFO(width=17, depth=256, r_domain="usb", w_domain="video")
        m.submodules += fifo

        # Pull out the sync events from the command byte
        hsync, vsync_odd, vsync_even, _ = taxi_decoder.command
        vsync = taxi_decoder.cstrb & (vsync_odd | vsync_even)

        # The camera sends 16bit samples in two 8bit chunks, LSB first
        # We keep track of the byte we're on and the previous byte,
        # to be recombined on pushing into the FIFO
        odd_byte = Signal()
        prev_byte = Signal(8)
        with m.If(taxi_decoder.dstrb):
            m.d.video += [
                prev_byte.eq(taxi_decoder.data),
                odd_byte.eq(~odd_byte),
            ]

        # Reset byte alignment state on vsync
        with m.If(vsync):
            m.d.video += odd_byte.eq(0)

        # If there's a 16bit sample ready, push it to the FIFO
        with m.If(taxi_decoder.dstrb & odd_byte):
            m.d.comb += [
                fifo.w_en.eq(1),
                fifo.w_data.eq(Cat(prev_byte, taxi_decoder.data)),
            ]
        # Or if there's a vsync event, push that
        with m.Elif(vsync):
            m.d.comb += [
                fifo.w_en.eq(1),
                fifo.w_data.eq(1<<16),
            ]

        m.d.comb += [
            fifo.r_en                .eq(stream_ep.stream.ready),
            stream_ep.stream.valid   .eq(fifo.r_rdy),
            stream_ep.stream.payload .eq(fifo.r_data[:16]),
            stream_ep.stream.last    .eq(fifo.r_data[16]),
        ]

        return m


if __name__ == "__main__":
    device = top_level_cli(ScorzoneraDevice)
