
import struct

from Event import Event
from Helper import writeVarLength


class NoteOff(Event):
    __hash__ = Event.__hash__
    evtname = 'NoteOff'
    midi_status = NOTE_OFF = 0x80
    sec_sort_order = 2

    def __init__(self, channel, pitch, tick, volume,
                 annotation=None, insertion_order=0):
        self.pitch = pitch
        self.volume = volume
        self.channel = channel
        self.annotation = annotation
        super(NoteOff, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.evtname == other.evtname and self.tick == other.tick and
                self.pitch == other.pitch and self.channel == other.channel)

    def __str__(self):
        return 'NoteOff %d at tick %d ch %d vel %d' % (
            self.pitch, self.tick, self.channel, self.volume)

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.pitch)
        midibytes += struct.pack('>B', self.volume)
        return midibytes
