import struct

from midiutil.Event.Events.ChannelPressure import ChannelPressure
from midiutil.Event.Events.Controller import Controller
from midiutil.Event.Events.Copyright import Copyright
from midiutil.Event.Events.KeySignature import KeySignature
from midiutil.Event.Events.NoteOff import NoteOff
from midiutil.Event.Events.NoteOn import NoteOn
from midiutil.Event.Events.PitchWheel import PitchWheel
from midiutil.Event.Events.ProgramChange import ProgramChange
from midiutil.Event.Events.SysEx import SysEx
from midiutil.Event.Events.Tempo import Tempo
from midiutil.Event.Events.Text import Text
from midiutil.Event.Events.TimeSignature import TimeSignature
from midiutil.Event.Events.TrackName import TrackName
from midiutil.Event.Events.UniversalSysEx import UniversalSysEx
from midiutil.Helper import *


class MIDITrack(object):
    def __init__(self, removeDuplicates, deinterleave):
        self.rmDups = removeDuplicates
        self.deinterleave = deinterleave
        self.eventList = []
        self.MIDIEventList = []
        self.MIDIData = b""
        self.dataLength = 0
        self.closed = False

    def addNoteByNumber(self, channel, pitch, tick, duration, volume, annotation=None, insertion_order=0):
        self.eventList.append(NoteOn(channel, pitch, tick, duration, volume, annotation=annotation, insertion_order=insertion_order))
        self.eventList.append(NoteOff(channel, pitch, tick + duration, volume, annotation=annotation, insertion_order=insertion_order))

    def addControllerEvent(self, channel, tick, controller_number, parameter, insertion_order=0):
        self.eventList.append(Controller(channel, tick, controller_number, parameter, insertion_order=insertion_order))

    def addPitchWheelEvent(self, channel, tick, pitch_wheel_value, insertion_order=0):
        self.eventList.append(PitchWheel(channel, tick, pitch_wheel_value, insertion_order=insertion_order))

    def addTempo(self, tick, tempo, insertion_order=0):
        self.eventList.append(Tempo(tick, tempo, insertion_order=insertion_order))

    def addSysEx(self, tick, manID, payload, insertion_order=0):
        self.eventList.append(SysEx(tick, manID, payload, insertion_order=insertion_order))

    def addUniversalSysEx(self, tick, code, subcode, payload, sysExChannel=0x7F, realTime=False, insertion_order=0):
        self.eventList.append(UniversalSysEx(tick, realTime, sysExChannel, code, subcode, payload, insertion_order=insertion_order))

    def addProgramChange(self, channel, tick, program, insertion_order=0):
        self.eventList.append(ProgramChange(channel, tick, program, insertion_order=insertion_order))

    def addChannelPressure(self, channel, tick, pressure_value, insertion_order=0):
        self.eventList.append(ChannelPressure(channel, tick, pressure_value, insertion_order=insertion_order))

    def addTrackName(self, tick, trackName, insertion_order=0):
        self.eventList.append(TrackName(tick, trackName, insertion_order=insertion_order))

    def addTimeSignature(self, tick, numerator, denominator, clocks_per_tick, notes_per_quarter, insertion_order=0):
        self.eventList.append(TimeSignature(tick, numerator, denominator, clocks_per_tick, notes_per_quarter, insertion_order=insertion_order))

    def addCopyright(self, tick, notice, insertion_order=0):
        self.eventList.append(Copyright(tick, notice, insertion_order=insertion_order))

    def addKeySignature(self, tick, accidentals, accidental_type, mode, insertion_order=0):
        self.eventList.append(KeySignature(tick, accidentals, accidental_type, mode, insertion_order=insertion_order))

    def addText(self, tick, text, insertion_order=0):
        self.eventList.append(Text(tick, text, insertion_order=insertion_order))

    def changeNoteTuning(self, tunings, sysExChannel=0x7F, realTime=True, tuningProgam=0, insertion_order=0):
        payload = struct.pack('>B', tuningProgam)
        payload = payload + struct.pack('>B', len(tunings))
        for (noteNumber, frequency) in tunings:
            payload = payload + struct.pack('>B', noteNumber)
            MIDIFreqency = frequencyToBytes(frequency)
            for byte in MIDIFreqency:
                payload = payload + struct.pack('>B', byte)

        self.eventList.append(UniversalSysEx(0, realTime, sysExChannel, 8, 2, payload, insertion_order=insertion_order))

    def processEventList(self):
        self.MIDIEventList = [evt for evt in self.eventList]
        self.MIDIEventList.sort(key=sortEvents)
        if self.deinterleave: self.deInterleaveNotes()

    def removeDuplicates(self):
        s = set(self.eventList)
        self.eventList = list(s)
        self.eventList.sort(key=sortEvents)

    def closeTrack(self):
        if self.closed: return
        self.closed = True
        if self.rmDups: self.removeDuplicates()
        self.processEventList()

    def writeMIDIStream(self):
        self.writeChronologicalEventsToStream()
        self.MIDIData += self.getCloseEvent()
        self.dataLength = self.getDataLength()

    def getDataLength(self):
        return struct.pack('>L', len(self.MIDIData))

    def getCloseEvent(self):
        return struct.pack('BBBB', 0x00, 0xFF, 0x2F, 0x00)

    def writeChronologicalEventsToStream(self):
        previous_event_tick = 0
        for event in self.MIDIEventList:
            self.MIDIData += event.serialize(previous_event_tick)

    def deInterleaveNotes(self):
        tempEventList = []
        stack = {}

        for event in self.MIDIEventList:
            if event.evtname in ['NoteOn', 'NoteOff']:
                noteeventkey = str(event.pitch) + str(event.channel)
                if event.evtname == 'NoteOn':
                    if noteeventkey in stack:
                        stack[noteeventkey].append(event.tick)
                    else:
                        stack[noteeventkey] = [event.tick]
                    tempEventList.append(event)
                elif event.evtname == 'NoteOff':
                    if len(stack[noteeventkey]) > 1:
                        event.tick = stack[noteeventkey].pop()
                        tempEventList.append(event)
                    else:
                        stack[noteeventkey].pop()
                        tempEventList.append(event)
            else:
                tempEventList.append(event)

        self.MIDIEventList = tempEventList
        self.MIDIEventList.sort(key=sortEvents)

    def adjustTimeAndOriginToBeRelative(self, origin, adjust):
        if len(self.MIDIEventList) == 0: return
        tempEventList = []
        internal_origin = origin if adjust else 0
        runningTick = 0

        for event in self.MIDIEventList:
            adjustedTick = event.tick - internal_origin
            event.tick = adjustedTick - runningTick
            runningTick = adjustedTick
            tempEventList.append(event)

        self.MIDIEventList = tempEventList

    def getHeader(self):
        return struct.pack('cccc', b'M', b'T', b'r', b'k')

    def writeTrack(self, fileHandle):
        fileHandle.write(self.getHeader())
        fileHandle.write(self.dataLength)
        fileHandle.write(self.MIDIData)
