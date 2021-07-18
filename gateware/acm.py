#
# This file is part of LUNA.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause

""" Pre-made gateware that implements CDC-ACM serial. """

from nmigen                            import Elaboratable, Module, Signal

from luna.gateware.stream                         import StreamInterface
from luna.gateware.usb.usb2.device                     import USBDevice
from luna.gateware.usb.usb2.request                    import USBRequestHandler, StallOnlyRequestHandler
from luna.gateware.usb.usb2.endpoints.stream           import USBStreamInEndpoint, USBStreamOutEndpoint

from usb_protocol.types                import USBRequestType
from usb_protocol.emitters             import DeviceDescriptorCollection
from usb_protocol.emitters.descriptors import cdc


class ACMRequestHandlers(USBRequestHandler):
    """ Minimal set of request handlers to implement ACM functionality.
    Implements just enough of the requests to be usable on major operating system.
    In testing, macOS and Linux are fine will all requests being stalled; while Windows
    seems to be happy as long as SET_LINE_CODING is implemented. We'll implement only
    that, and stall every other handler.
    """

    SET_LINE_CODING = 0x20

    def elaborate(self, platform):
        m = Module()

        interface         = self.interface
        setup             = self.interface.setup

        #
        # Class request handlers.
        #

        with m.If(setup.type == USBRequestType.CLASS):
            with m.Switch(setup.request):

                # SET_LINE_CODING: The host attempts to tell us how it wants serial data
                # encoding. Since we output a stream, we'll ignore the actual line coding.
                with m.Case(self.SET_LINE_CODING):

                    # Always ACK the data out...
                    with m.If(interface.rx_ready_for_response):
                        m.d.comb += interface.handshakes_out.ack.eq(1)

                    # ... and accept whatever the request was.
                    with m.If(interface.status_requested):
                        m.d.comb += self.send_zlp()


                with m.Case():

                    #
                    # Stall unhandled requests.
                    #
                    with m.If(interface.status_requested | interface.data_requested):
                        m.d.comb += interface.handshakes_out.stall.eq(1)

                return m


class USBSerialInterface(Elaboratable):
    """ Interface that acts as a CDC-ACM 'serial converter'.
    Exposes a stream interface.
    Attributes
    ----------
    rx: StreamInterface(), output stream
        A stream carrying data received from the host.
    tx: StreamInterface(), input stream
        A stream carrying data to be transmitted to the host.
    Parameters
    ----------
    usb: USBDevice
    control_ep: USBControlEndpoint
    max_packet_size: int in {64, 246, 512}, optional
        The maximum packet size for communications.
    """


    def __init__(self, *, max_packet_size=64):
        self._max_packet_size     = max_packet_size
        self._status_endpoint_number = 3
        self._data_endpoint_number   = 4

        #
        # I/O port
        #
        self.rx      = StreamInterface()
        self.tx      = StreamInterface()


    def add_descriptors(self, config_descriptor):
        """ Adds the descriptors that describe our serial topology. """

        # First, we'll describe the Communication Interface, which contains most
        # of our description; but also an endpoint that does effectively nothing in
        # our case, since we don't have interrupts we want to send up to the host.
        with config_descriptor.InterfaceDescriptor() as i:
            i.bInterfaceNumber   = 0

            i.bInterfaceClass    = 0x02 # CDC
            i.bInterfaceSubclass = 0x02 # ACM
            i.bInterfaceProtocol = 0x01 # AT commands / UART

            # Provide the default CDC version.
            i.add_subordinate_descriptor(cdc.HeaderDescriptorEmitter())

            # ... specify our interface associations ...
            union = cdc.UnionFunctionalDescriptorEmitter()
            union.bControlInterface      = 0
            union.bSubordinateInterface0 = 1
            i.add_subordinate_descriptor(union)

            # ... and specify the interface that'll carry our data...
            call_management = cdc.CallManagementFunctionalDescriptorEmitter()
            call_management.bDataInterface = 1
            i.add_subordinate_descriptor(call_management)

            # CDC communications endpoint
            with i.EndpointDescriptor() as e:
                e.bEndpointAddress = 0x80 | self._status_endpoint_number
                e.bmAttributes     = 0x03
                e.wMaxPacketSize   = self._max_packet_size
                e.bInterval        = 11

        # Finally, we'll describe the communications interface, which just has the
        # endpoints for our data in and out.
        with config_descriptor.InterfaceDescriptor() as i:
            i.bInterfaceNumber   = 1
            i.bInterfaceClass    = 0x0a # CDC data
            i.bInterfaceSubclass = 0x00
            i.bInterfaceProtocol = 0x00

            # Data IN to host (tx, from our side)
            with i.EndpointDescriptor() as e:
                e.bEndpointAddress = 0x80 | self._data_endpoint_number
                e.wMaxPacketSize   = self._max_packet_size

            # Data OUT from host (rx, from our side)
            with i.EndpointDescriptor() as e:
                e.bEndpointAddress = self._data_endpoint_number
                e.wMaxPacketSize   = self._max_packet_size


    def add_handlers(self, control_ep):
        # Attach our class request handlers.
        control_ep.add_request_handler(ACMRequestHandlers())

        # Attach class-request handlers that stall any vendor or reserved requests,
        # as we don't have or need any.
        stall_condition = lambda setup : \
            (setup.type == USBRequestType.VENDOR) | \
            (setup.type == USBRequestType.RESERVED)
        control_ep.add_request_handler(StallOnlyRequestHandler(stall_condition))


    def add_endpoints(self, usb):
        # Create our status/communications endpoint; but don't ever drive its stream.
        # This should be optimized down to an endpoint that always NAKs.
        self._serial_status_ep = USBStreamInEndpoint(
            endpoint_number=self._status_endpoint_number,
            max_packet_size=self._max_packet_size
        )
        usb.add_endpoint(self._serial_status_ep)

        # Create an endpoint for serial rx...
        self._serial_rx_endpoint = USBStreamOutEndpoint(
            endpoint_number=self._data_endpoint_number,
            max_packet_size=self._max_packet_size,
        )
        usb.add_endpoint(self._serial_rx_endpoint)

        # ... and one for serial tx.
        self._serial_tx_endpoint = USBStreamInEndpoint(
            endpoint_number=self._data_endpoint_number,
            max_packet_size=self._max_packet_size
        )
        usb.add_endpoint(self._serial_tx_endpoint)


    def elaborate(self, platform):
        m = Module()

        # Connect up our I/O.
        m.d.comb += [
            self._serial_tx_endpoint.stream  .stream_eq(self.tx),
            self.rx                    .stream_eq(self._serial_rx_endpoint.stream),
        ]

        return m
