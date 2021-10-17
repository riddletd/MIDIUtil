class Event(object):
    evtname = None
    sec_sort_order = 0

    def __init__(self, tick, insertion_order):
        self.tick = tick
        self.insertion_order = insertion_order

    def __eq__(self, other):
        return (self.evtname == other.evtname and self.tick == other.tick)

    def __hash__(self):
        a = int(self.tick)
        a = (a + 0x7ed55d16) + (a << 12)
        a = (a ^ 0xc761c23c) ^ (a >> 19)
        a = (a + 0x165667b1) + (a << 5)
        a = (a + 0xd3a2646c) ^ (a << 9)
        a = (a + 0xfd7046c5) + (a << 3)
        a = (a ^ 0xb55a4f09) ^ (a >> 16)
        return a
