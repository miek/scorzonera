from amaranth import *
from amaranth.sim import Simulator
import unittest

# [Table 2, Page 15; TAXIchip datasheet]
taxi_commands = [
    "JK",
    "II",
    "TT",
    "TS",
    "IH",
    "TR",
    "SR",
    "SS",
    "HH",
    "HI",
    "HQ",
    "RR",
    "RS",
    "QH",
    "QI",
    "QQ",
]

# [Table 2, Page 15; TAXIchip datasheet]
symbols_4b5b_command = {
    'H': 0b00100,
    'I': 0b11111,
    'J': 0b11000,
    'K': 0b10001,
    'L': 0b00110,
    'Q': 0b00000,
    'R': 0b00111,
    'S': 0b11001,
    'T': 0b01101,
}

# 4b5b encoding map [Table 1, Page 14; TAXIchip datasheet]
symbols_4b5b_data = [
    0b11110,
    0b01001,
    0b10100,
    0b10101,
    0b01010,
    0b01011,
    0b01110,
    0b01111,
    0b10010,
    0b10011,
    0b10110,
    0b10111,
    0b11010,
    0b11011,
    0b11100,
    0b11101,
]

def get_command_pattern(command):
    return symbols_4b5b_command[command[1]] | (symbols_4b5b_command[command[0]] << 5)

SYNC = get_command_pattern(taxi_commands[0])

class DecodeTaxiCommand(Elaboratable):
    def __init__(self):
        self.input = Signal(10)
        self.output = Signal(4)
        self.valid = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.input):
            for data, command in enumerate(taxi_commands):
                pattern = get_command_pattern(command)
                with m.Case(pattern):
                    m.d.comb += self.output.eq(data)
                    m.d.comb += self.valid.eq(1)

        return m


class Decode4B5BData(Elaboratable):
    def __init__(self):
        self.input = Signal(5)
        self.output = Signal(4)
        self.valid = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.input):
            for data, symbol in enumerate(symbols_4b5b_data):
                with m.Case(symbol):
                    m.d.comb += self.output.eq(data),
                    m.d.comb += self.valid.eq(1)

        return m


class TaxiDecoder(Elaboratable):
    """

    I/O port:
        I: symbol
        I: symbol_valid
        O: violation
        O: cstrb
        O: command
        O: dstrb
        O: data

    """
    def __init__(self):
        self.symbol = Signal(10)
        self.symbol_valid = Signal()
        self.violation = Signal()
        self.cstrb = Signal()
        self.command = Signal(4)
        self.dstrb = Signal()
        self.data = Signal(8)

    def elaborate(self, platform):
        m = Module()

        # Command
        m.submodules.command = DecodeTaxiCommand()
        command_valid = self.symbol_valid & m.submodules.command.valid
        m.d.comb += m.submodules.command.input.eq(self.symbol)
        m.d.sync += self.command.eq(m.submodules.command.output)
        m.d.sync += self.cstrb.eq(command_valid)

        # Data
        data_MSn = Decode4B5BData()
        m.submodules.data_MSn = data_MSn

        data_LSn = Decode4B5BData()
        m.submodules.data_LSn = data_LSn

        data_valid = self.symbol_valid & data_MSn.valid & data_LSn.valid

        m.d.comb += Cat(data_LSn.input, data_MSn.input).eq(self.symbol)
        m.d.sync += self.data.eq(Cat(data_LSn.output, data_MSn.output))
        m.d.sync += self.dstrb.eq(data_valid)

        m.d.sync += self.violation.eq(self.symbol_valid & ~(data_valid | command_valid))

        return m


class TestTaxi(unittest.TestCase):
    def test_taxi(self):
        taxi = TaxiDecoder()

        sim = Simulator(taxi)
        sim.add_clock(1/160e6)

        def process():
            commands_seen = []
            data_seen = []
            yield taxi.symbol_valid.eq(1)
            # Loop through all 10bit symbols
            for i in range(2**10):
                yield taxi.symbol.eq(i)
                yield
                yield
                if (yield taxi.dstrb):
                    data = yield taxi.data
                    # Check for unique data output
                    self.assertNotIn(data, data_seen)
                    data_seen.append(data)
                if (yield taxi.cstrb):
                    command = yield taxi.command
                    # Check for unique command output
                    self.assertNotIn(command, commands_seen)
                    commands_seen.append(command)

            # Check we saw all possible commands / data
            self.assertEqual(len(commands_seen), 16)
            self.assertEqual(len(data_seen), 256)

        sim.add_sync_process(process)
        #with sim.write_vcd("taxi-decode.vcd", "taxi-decode.gtkw", traces=[]):
        sim.run()


if __name__ == "__main__":
    unittest.main()

