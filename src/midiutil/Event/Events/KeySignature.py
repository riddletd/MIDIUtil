
import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class KeySignature(Event):
    evtname = 'KeySignature'
    sec_sort_order = 1

    def __init__(self, tick, accidentals, accidental_type, mode,
                 insertion_order=0):
        self.accidentals = accidentals
        self.accidental_type = accidental_type
        self.mode = mode
        super(KeySignature, self).__init__(tick, insertion_order)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xFF
        subcode = 0x59
        event_subtype = 0x02
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', subcode)
        midibytes += struct.pack('>B', event_subtype)
        midibytes += struct.pack('>b', self.accidentals * self.accidental_type)
        midibytes += struct.pack('>B', self.mode)
        return midibytes
