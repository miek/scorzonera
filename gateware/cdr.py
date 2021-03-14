from nmigen import *
from nmigen.back.pysim import Simulator
from nmigen.build import *
from nmigen.cli import main
import numpy as np
import unittest


class CDR(Elaboratable):
    """ Data recovery

    Take 4x oversampled input and return the recovered data stream.
    Returns 0, 1 or 2 valid bits on each cycle

    I/O port:
        I: input        -- Oversampled input data. LSB represents earliest sample, MSB represents latest sample.
        O: data         -- Output data. MSB represents earliest sample, LSB represents latest sample. (this should probably change to match input))
        O: data_valid   -- Mask for `data`.
        O: initial_lock -- Goes high on first sampling domain selection.
    """
    def __init__(self):
        self.input = Signal(4)
        self.data = Signal(2)
        self.data_valid = Signal(2)
        self.initial_lock = Signal()
        self._selected_domain = Signal.like(self.input)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        prev_input = Signal.like(self.input)

        rising  = Signal.like(self.input)
        falling = Signal.like(self.input)

        domain_sel = Signal.like(self.input)
        selected_domain = Signal.like(self.input)
        m.d.comb += self._selected_domain.eq(selected_domain)

        m.d.sync += [
            prev_input.eq(self.input),

            # Find rising/falling edges for each domain
            rising .eq((self.input ^ prev_input) & self.input),
            falling.eq((self.input & prev_input) & ~self.input),

            # Edge first seen on 2, sample on 0
            domain_sel[0].eq((rising == 0b0011) | (falling == 0b0011)),

            # Edge first seen on 3, sample on 1
            domain_sel[1].eq((rising == 0b0111) | (falling == 0b0111)),

            # Edge first seen on 0, sample on 2
            domain_sel[2].eq((rising == 0b1111) | (falling == 0b1111)),

            # Edge first seen on 1, sample on 3
            domain_sel[3].eq((rising == 0b0001) | (falling == 0b0001)),
        ]

        m.d.comb += [
            self.data[0].eq((prev_input & selected_domain) != 0),
            self.data[1].eq((prev_input[0] & selected_domain[3]) | (prev_input[3] & selected_domain[0])),
        ]

        with m.If(domain_sel != 0):
            m.d.sync += selected_domain.eq(domain_sel)
            m.d.sync += self.initial_lock.eq(1)

        # Moving from domain 3 -> 0
        with m.If(selected_domain[3] & domain_sel[0]):
            m.d.sync += self.data_valid.eq(0b00)
        # Moving from domain 0 -> 3
        with m.Elif(selected_domain[0] & domain_sel[3]):
            m.d.sync += self.data_valid.eq(0b11)
        with m.Else():
            m.d.sync += self.data_valid.eq(0b01)

        return m


class TestCDR(unittest.TestCase):
    def run_sim(self, drift_period=50, insert=True):
        cdr = CDR()

        sim = Simulator(cdr)
        sim.add_clock(1/160e6)

        def prepare_samples(data, drift_period, insert=True):
            # oversample x4
            samples = np.repeat(data, 4)

            drift_counter = 0
            l = len(samples)

            # reduce length if we're about to delete a bunch of samples
            if not insert:
                l -= len(samples) // drift_period

            for i in range(l):
                # insert/delete a sample every `drift_period` samples to simulate a clock rate mismatch
                if drift_counter == drift_period:
                    if insert:
                        samples = np.insert(samples, i, [samples[i-1]])
                    else:
                        samples = np.delete(samples, i)
                    drift_counter = 0
                    continue
                drift_counter += 1

            # trim length to a multiple of 4, then return data in 4-sample groups
            return np.reshape(samples[:len(samples)-(len(samples)%4)], (-1, 4)).tolist()


        def process():
            data = [1,0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0]*20
            out = []
            skip = 0
            samples = prepare_samples(data, drift_period, insert)
            for s in samples:
                yield cdr.input.eq(Cat(s[0], s[1], s[2], s[3]))
                yield
                lock = yield cdr.initial_lock
                dv = yield cdr.data_valid
                d = yield cdr.data
                if lock:
                    if dv == 0b01:
                        out.append(d & 1)
                    elif dv == 0b11:
                        out += [(d & 2) >> 1, d & 1]
                else:
                    skip += 1

            # skip data before initial lock
            # also account for 1-cycle latency
            self.assertTrue(data[skip:-1] == out[1:])

        sim.add_sync_process(process)
        #with sim.write_vcd("cdr.vcd", "cdr.gtkw", traces=[]):
        sim.run()

    def test_no_drift(self):
        self.run_sim(drift_period=-1)

    def test_inserted_samples(self):
        self.run_sim(insert=True)

    def test_deleted_samples(self):
        self.run_sim(insert=False)


class SymbolSynchroniser(Elaboratable):
    """
    I/O port:
        I: input        -- 2-bit input
        I: input_valid  -- Mask for `input`.
        I: resync       -- Force resync
        O: symbol       -- 10bit symbol
        O: symbol_valid -- Symbol valid
    """
    def __init__(self, sync_symbol):
        self._sync_symbol  = sync_symbol
        self._symbol_size  = sync_symbol.width
        assert self._symbol_size == 10

        self.input         = Signal(2)
        self.input_valid   = Signal(2)
        self.resync        = Signal()
        self.symbol        = Signal(self._symbol_size)
        self.symbol_valid  = Signal()

        self._synced       = Signal()
        self._buffer       = Signal(self._symbol_size+1, reset=0)
        self._buffer_count = Signal(range(self._symbol_size+1+1))


    def elaborate(self, platform):
        m = Module()

        # Shift in any available bits.
        shift_count = Signal(2)
        with m.Switch(self.input_valid):
            with m.Case(0b11):
                m.d.sync += self._buffer.eq(Cat(self.input   , self._buffer[:-2]))
                m.d.comb += shift_count.eq(2)

            with m.Case(0b01):
                m.d.sync += self._buffer.eq(Cat(self.input[0], self._buffer[:-1]))
                m.d.comb += shift_count.eq(1)

            with m.Default():
                m.d.comb += shift_count.eq(0)

        # Default to no valid symbol
        m.d.sync += self.symbol_valid.eq(0)

        # In sync, see if there are enough valid bits to output a symbol:
        with m.If(self._synced & ~self.resync):

            with m.Switch(self._buffer_count):

                # We have one spare bit (the LSB) for a future symbol.
                with m.Case(self._symbol_size + 1):
                    m.d.sync += [
                        # Output the most significant bits
                        self.symbol         .eq(self._buffer[1:]),
                        self.symbol_valid   .eq(1),

                        # ... and update the valid-count (1 spare bit + any shifted in this cycle).
                        self._buffer_count  .eq(1 + shift_count),
                    ]

                # We have exactly the right number of valid bits.
                with m.Case(self._symbol_size):
                    m.d.sync += [
                        # Output the valid bits
                        self.symbol         .eq(self._buffer[:-1]),
                        self.symbol_valid   .eq(1),

                        # ... and reset the valid count.
                        self._buffer_count  .eq(shift_count),
                    ]

                # Otherwise, just increment the valid counter.
                with m.Default():
                    m.d.sync += self._buffer_count.eq(self._buffer_count + shift_count)


        # Not in sync, look for a sync symbol:
        with m.Else():
            m.d.sync += self._synced.eq(0)
            with m.If(self._buffer[1:] == self._sync_symbol):
                m.d.sync += [
                    self._buffer_count  .eq(1 + shift_count),
                    self._synced        .eq(1),
                    self.symbol         .eq(self._sync_symbol),
                    self.symbol_valid   .eq(1),
                ]

            with m.Elif(self._buffer[:-1] == self._sync_symbol):
                m.d.sync += [
                    self._buffer_count  .eq(shift_count),
                    self._synced        .eq(1),
                    self.symbol         .eq(self._sync_symbol),
                    self.symbol_valid   .eq(1),
                ]

        return m


class TestSync(unittest.TestCase):
    def test_sync(self):
        synchroniser = SymbolSynchroniser(sync_symbol=Const(0b1100010001))

        sim = Simulator(synchroniser)
        sim.add_clock(1/160e6)

        def bits(value, width=10):
            return [(value >> (width-1-i)) & 1 for i in range(width)]

        def process():
            sync_symbol = [1, 1, 0, 0, 0, 1, 0, 0, 0, 1]
            data = sync_symbol
            symbol_count = 100
            for i in range(1, symbol_count):
                data += bits(i)
            data += [0, 0]

            # Check we start with no sync, no valid symbol, and it's stable for a while.
            for i in range(20):
                yield
                self.assertEqual((yield synchroniser._synced),      0)
                self.assertEqual((yield synchroniser.symbol_valid), 0)

            count = 0
            for bit in data:
                yield synchroniser.input[0].eq(bit)
                yield synchroniser.input_valid.eq(1)
                yield
                if ((yield synchroniser.symbol_valid)):
                    if count == 0:
                        expected_symbol = 0b1100010001
                    else:
                        expected_symbol = count
                    self.assertEqual((yield synchroniser.symbol), expected_symbol)
                    count += 1

            self.assertEqual(count, symbol_count)


        sim.add_sync_process(process)
        with sim.write_vcd("sync.vcd", "sync.gtkw", traces=[]):
            sim.run()


if __name__ == "__main__":
    unittest.main()

