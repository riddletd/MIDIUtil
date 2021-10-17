import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class TimeSignature(Event):
    evtname = 'TimeSignature'
    sec_sort_order = 0

    def __init__(self, tick, numerator, denominator, clocks_per_tick,
                 notes_per_quarter, insertion_order=0):
        self.numerator = numerator
        self.denominator = denominator
        self.clocks_per_tick = clocks_per_tick
        self.notes_per_quarter = notes_per_quarter
        super(TimeSignature, self).__init__(tick, insertion_order)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xFF
        subcode = 0x58
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', subcode)
        midibytes += struct.pack('>B', 0x04)
        midibytes += struct.pack('>B', self.numerator)
        midibytes += struct.pack('>B', self.denominator)
        midibytes += struct.pack('>B', self.clocks_per_tick)
        midibytes += struct.pack('>B', self.notes_per_quarter)
        return midibytes
