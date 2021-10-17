import struct

from Event import Event
from Helper import writeVarLength


class TrackName(Event):
    __hash__ = Event.__hash__
    evtname = 'TrackName'
    sec_sort_order = 0

    def __init__(self, tick, trackName, insertion_order=0):
        self.trackName = trackName.encode("ISO-8859-1")
        super(TrackName, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and
                self.tick == other.tick and
                self.trackName == other.trackName)

    def serialize(self, previous_event_tick):
        midibytes = b""
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('B', 0xFF)
        midibytes += struct.pack('B', 0X03)
        dataLength = len(self.trackName)
        dataLengthVar = writeVarLength(dataLength)
        for i in dataLengthVar:
            midibytes += struct.pack("B", i)
        midibytes += self.trackName
        return midibytes
