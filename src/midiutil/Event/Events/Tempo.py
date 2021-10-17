import struct

from Event import Event
from Helper import writeVarLength


class Tempo(Event):
    __hash__ = Event.__hash__
    evtname = 'Tempo'
    sec_sort_order = 3

    def __init__(self, tick, tempo, insertion_order=0):
        self.tempo = int(60000000 / tempo)
        super(Tempo, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and
                self.tick == other.tick and
                self.tempo == other.tempo)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = 0xFF
        subcode = 0x51
        fourbite = struct.pack('>L', self.tempo)
        threebite = fourbite[1:4]
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', subcode)
        midibytes += struct.pack('>B', 0x03)
        midibytes += threebite
        return midibytes
