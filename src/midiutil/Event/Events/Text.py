import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class Text(Event):
    evtname = 'Text'
    sec_sort_order = 1

    def __init__(self, tick, text, insertion_order=0):
        self.text = text.encode("ISO-8859-1")
        super(Text, self).__init__(tick, insertion_order)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xFF
        subcode = 0x01
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', subcode)
        payloadLength = len(self.text)
        payloadLengthVar = writeVarLength(payloadLength)
        for i in payloadLengthVar:
            midibytes += struct.pack("B", i)
        midibytes += self.text
        return midibytes
