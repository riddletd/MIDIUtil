import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class ProgramChange(Event):
    __hash__ = Event.__hash__
    evtname = 'ProgramChange'
    midi_status = PROGRAM_CHANGE = 0xc0
    sec_sort_order = 1

    def __init__(self, channel, tick, programNumber,
                 insertion_order=0):
        self.programNumber = programNumber
        self.channel = channel
        super(ProgramChange, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and
                self.tick == other.tick and
                self.programNumber == other.programNumber and
                self.channel == other.channel)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.programNumber)
        return midibytes
