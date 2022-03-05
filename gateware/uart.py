from amaranth import Cat, Elaboratable, Module, Signal
from luna.gateware.stream import StreamInterface


class UARTRx(Elaboratable):
    """ UART receiver module.

    Attributes
    ----------
    rx: StreamInterface(), output stream
        A stream carrying data received from the remote device.
    rx_pin: Signal(), input RX pin
        Input signal from the UART RX pin.

    Parameters
    ----------
    baud_rate: int
    clock_rate: int
    """


    def __init__(self, baud_rate=19200, clock_rate=60e6):
        self._baud_rate = baud_rate
        self._clock_rate = clock_rate
        self._bits = 8

        #
        # I/O port
        #
        self.rx      = StreamInterface(payload_width=self._bits)
        self.rx_pin  = Signal()


    def elaborate(self, platform):
        m = Module()

        # Calculate number of clock cycles for each bit,
        # and create a counter to keep track of when to sample.
        bit_time      = int(self._clock_rate / self._baud_rate)
        counter       = Signal(range(bit_time + 1))
        sample_strobe = (counter == bit_time)
        m.d.sync     += counter.eq(counter + 1)

        # Counter & storage for incoming data bits
        bit_count = Signal(range(self._bits))
        data      = Signal(self._bits)

        # Default to no data ready.
        m.d.sync += self.rx.valid.eq(0)

        # Flush on new-line
        m.d.comb += self.rx.last.eq(self.rx.payload == ord("\n"))

        with m.FSM() as fsm:
            # Waiting for first RX falling edge.
            with m.State("IDLE"):
                with m.If(~self.rx_pin):
                    # After initial RX edge, sample again in the centre of the bit time
                    m.d.sync += counter.eq(int(bit_time / 2))
                    m.next = "START"

            # Waiting to sample the start bit.
            with m.State("START"):
                with m.If(sample_strobe):
                    with m.If(~self.rx_pin):
                        m.d.sync += [
                            counter.eq(0),
                            bit_count.eq(0),
                        ]
                        m.next = "DATA"

                    with m.Else():
                        # TODO: flag error?
                        m.next = "IDLE"

            # Waiting to sample data bits.
            with m.State("DATA"):
                with m.If(sample_strobe):
                    # Sample data bit, shift into `data` and reset for the next bit.
                    m.d.sync += [
                        data.eq(Cat(data[1:], self.rx_pin)),
                        counter.eq(0),
                        bit_count.eq(bit_count + 1),
                    ]
                    with m.If(bit_count == self._bits - 1):
                        m.next = "STOP"

            # Waiting to sample the stop bit.
            with m.State("STOP"):
                with m.If(sample_strobe):
                    with m.If(self.rx_pin):
                        m.d.sync += [
                            self.rx.payload.eq(data),
                            self.rx.valid.eq(1),
                        ]

                    with m.Else():
                        # TODO: flag framing error?
                        pass

                    m.next = "IDLE"


        return m


class UARTTx(Elaboratable):
    """ UART transmitter module.

    Attributes
    ----------
    tx: StreamInterface(), input stream
        A stream carrying data to be transmitted to the remote device.
    tx_pin: Signal(), output TX pin
        Output signal to the UART TX pin.

    Parameters
    ----------
    baud_rate: int
    clock_rate: int
    """


    def __init__(self, baud_rate=19200, clock_rate=60e6):
        self._baud_rate = baud_rate
        self._clock_rate = clock_rate
        self._bits = 8

        #
        # I/O port
        #
        self.tx      = StreamInterface(payload_width=self._bits)
        self.tx_pin  = Signal()


    def elaborate(self, platform):
        m = Module()

        # Calculate number of clock cycles for each bit.
        bit_time      = int(self._clock_rate / self._baud_rate)
        counter       = Signal(range(bit_time + 1))
        tx_strobe     = (counter == bit_time)
        m.d.sync     += counter.eq(counter + 1)

        # Counter & storage for outgoing data bits
        bits      = self._bits + 1
        bit_count = Signal(range(bits+1))
        data      = Signal(bits)

        # Default to not reading from the stream.
        m.d.sync += self.tx.ready.eq(0)

        with m.FSM() as fsm:
            # Waiting for data from the stream.
            with m.State("IDLE"):
                # Idle high.
                self.tx_pin.eq(1)

                with m.If(self.tx.valid):
                    m.d.sync += [
                        # Send start bit.
                        self.tx_pin.eq(0),

                        # Read a byte from the stream, adding the stop bit on the end.
                        data.eq(Cat(self.tx.payload, 1)),
                        self.tx.ready.eq(1),

                        # and setup counters.
                        counter.eq(0),
                        bit_count.eq(0),
                    ]
                    m.next = "TX"

            # Shifting out bits.
            with m.State("TX"):
                with m.If(tx_strobe):
                    with m.If(bit_count == bits):
                        m.next = "IDLE"
                    with m.Else():
                        m.d.sync += [
                            data.eq(Cat(data[1:])),
                            self.tx_pin.eq(data[0]),
                            counter.eq(0),
                            bit_count.eq(bit_count + 1),
                        ]


        return m
