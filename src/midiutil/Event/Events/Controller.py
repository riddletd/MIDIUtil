import struct

from midiutil.Event.Event import Event
from midiutil.Helper import writeVarLength


class Controller(Event):
    __hash__ = Event.__hash__
    evtname = 'Controller'
    midi_status = CONTROL_CHANGE = 0xB0
    sec_sort_order = 1

    def __init__(self, channel, tick, controller_number, parameter,
                 insertion_order=0):
        self.parameter = parameter
        self.channel = channel
        self.controller_number = controller_number
        super(Controller, self).__init__(tick, insertion_order)

    def __eq__(self, other):
        return False

    def serialize(self, previous_event_tick):
        midibytes = b""
        code = self.midi_status | self.channel
        varTime = writeVarLength(self.tick - previous_event_tick)
        for timeByte in varTime:
            midibytes += struct.pack('>B', timeByte)
        midibytes += struct.pack('>B', code)
        midibytes += struct.pack('>B', self.controller_number)
        midibytes += struct.pack('>B', self.parameter)
        return midibytes
