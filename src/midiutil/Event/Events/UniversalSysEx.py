import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class UniversalSysEx(Event):
    evtname = 'UniversalSysEx'
    sec_sort_order = 1

    def __init__(self, tick, realTime, sysExChannel, code, subcode,
                 payload, insertion_order=0):
        self.realTime = realTime
        self.sysExChannel = sysExChannel
        self.code = code
        self.subcode = subcode
        self.payload = payload
        super(UniversalSysEx, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return False

    __hash__ = Event.__hash__

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xF0
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        payloadLength = writeVarLength(len(self.payload) + 5)
        for lenByte in payloadLength:
            midibytes += struct.pack('>B', lenByte)

        if self.realTime:
            midibytes += struct.pack('>B', 0x7F)
        else:
            midibytes += struct.pack('>B', 0x7E)

        midibytes += struct.pack('>B', self.sysExChannel)
        midibytes += struct.pack('>B', self.code)
        midibytes += struct.pack('>B', self.subcode)
        midibytes += self.payload
        midibytes += struct.pack('>B', 0xF7)
        return midibytes
