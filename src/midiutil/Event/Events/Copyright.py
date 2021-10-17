import struct

from midiutil.Event.Event import Event

from ...Helper import writeVarLength


class Copyright(Event):
    evtname = 'Copyright'
    sec_sort_order = 1

    def __init__(self, tick, notice, insertion_order=0):
        self.notice = notice.encode("ISO-8859-1")
        super(Copyright, self).__init__(tick, insertion_order)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xFF
        subcode = 0x02
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', subcode)
        payloadLength = len(self.notice)
        payloadLengthVar = writeVarLength(payloadLength)
        for i in payloadLengthVar:
            midibytes += struct.pack("b", i)
        midibytes += self.notice
        return midibytes
