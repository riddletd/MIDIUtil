import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class PitchWheel(Event):
    __hash__ = Event.__hash__
    evtname = 'PitchWheel'
    midi_status = PITCH_WHEEL_CHANGE = 0xE0
    sec_sort_order = 1

    def __init__(self, channel, tick, pitch_wheel_value, insertion_order=0):
        self.channel = channel
        self.pitch_wheel_value = pitch_wheel_value
        super(PitchWheel, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return False

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes = midibytes + struct.pack('>B', timeByte)
        MSB = (self.pitch_wheel_value + 8192) >> 7
        LSB = (self.pitch_wheel_value + 8192) & 0x7F
        midibytes = midibytes + struct.pack('>B', code)
        midibytes = midibytes + struct.pack('>B', LSB)
        midibytes = midibytes + struct.pack('>B', MSB)
        return midibytes
