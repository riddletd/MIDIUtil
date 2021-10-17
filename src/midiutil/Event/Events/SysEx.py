import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class SysEx(Event):
    __hash__ = Event.__hash__
    evtname = 'SysEx'
    sec_sort_order = 1

    def __init__(self, tick, manID, payload, insertion_order=0):
        self.manID = manID
        self.payload = payload
        super(SysEx, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return False

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xF0
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)

        payloadLength = writeVarLength(len(self.payload) + 2)
        for lenByte in payloadLength:
            midibytes += struct.pack('>B', lenByte)

        midibytes += struct.pack('>B', self.manID)
        midibytes += self.payload
        midibytes += struct.pack('>B', 0xF7)
        return midibytes
