import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class ChannelPressure(Event):
    __hash__ = Event.__hash__
    evtname = 'ChannelPressure'
    midi_status = ChannelPressure = 0xD0
    sec_sort_order = 1

    def __init__(self, channel, tick, pressure_value, insertion_order=0):
        self.channel = channel
        self.pressure_value = pressure_value
        super(ChannelPressure, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return (self.__class__.__name__ == other.__class__.__name__ and
                self.tick == other.tick and
                self.pressure_value == other.pressure_value and
                self.channel == other.channel)


    def serialize(self, previous_event_tick):
        midibytes = b""
        code = self.midi_status | self.channel
        vartick = writeVarLength(self.tick - previous_event_tick)
        for x in vartick:
            midibytes += struct.pack('>B', x)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.pressure_value)
        return midibytes
