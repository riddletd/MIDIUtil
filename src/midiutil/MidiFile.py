from __future__ import division

from Helper import sort_events
from MIDIHeader import MIDIHeader
from MIDITrack import MIDITrack

controllerEventTypes = {'pan': 0x0a}
QUARTER_NOTE_TICKS = 960
MAJOR = 0
MINOR = 1
SHARPS = 1
FLATS = -1

class MIDIFile(object):
    def __init__(self, numTracks=1, removeDuplicates=True, deinterleave=True,
                 adjust_origin=False, file_format=1,
                 ticks_per_quarternote=QUARTER_NOTE_TICKS, eventtime_is_ticks=False):
        self.tracks = list()
        if file_format == 1:
            self.numTracks = numTracks + 1
        else:
            self.numTracks = numTracks
        self.header = MIDIHeader(self.numTracks, file_format, ticks_per_quarternote)

        self.adjust_origin = adjust_origin
        self.closed = False

        self.ticks_per_quarternote = ticks_per_quarternote
        self.eventtime_is_ticks = eventtime_is_ticks
        if self.eventtime_is_ticks:
            self.time_to_ticks = lambda x: x
        else:
            self.time_to_ticks = self.quarter_to_tick

        for i in range(0, self.numTracks):
            self.tracks.append(MIDITrack(removeDuplicates, deinterleave))
        self.event_counter = 0

    def quarter_to_tick(self, quarternote_time):
        return int(quarternote_time * self.ticks_per_quarternote)

    def tick_to_quarter(self, ticknum):
        return float(ticknum) / self.ticks_per_quarternote

    def addNote(self, track, channel, pitch, time, duration, volume,
                annotation=None):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addNoteByNumber(channel, pitch,
                                           self.time_to_ticks(time), self.time_to_ticks(duration),
                                           volume, annotation=annotation,
                                           insertion_order=self.event_counter)
        self.event_counter += 1

    def addTrackName(self, track, time, trackName):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addTrackName(self.time_to_ticks(time), trackName,
                                        insertion_order=self.event_counter)
        self.event_counter += 1

    def addTimeSignature(self, track, time, numerator, denominator,
                         clocks_per_tick, notes_per_quarter=8):
        if self.header.numeric_format == 1:
            track = 0

        self.tracks[track].addTimeSignature(self.time_to_ticks(time), numerator, denominator,
                                            clocks_per_tick, notes_per_quarter,
                                            insertion_order=self.event_counter)
        self.event_counter += 1

    def addTempo(self, track, time, tempo):
        if self.header.numeric_format == 1:
            track = 0
        self.tracks[track].addTempo(self.time_to_ticks(time), tempo,
                                    insertion_order=self.event_counter)
        self.event_counter += 1

    def addCopyright(self, track, time, notice):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addCopyright(self.time_to_ticks(time), notice,
                                        insertion_order=self.event_counter)
        self.event_counter += 1

    def addKeySignature(self, track, time, accidentals, accidental_type, mode,
                        insertion_order=0):
        if self.header.numeric_format == 1:
            track = 0  
        self.tracks[track].addKeySignature(self.time_to_ticks(time), accidentals, accidental_type,
                                           mode, insertion_order=self.event_counter)
        self.event_counter += 1

    def addText(self, track, time, text):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addText(self.time_to_ticks(time), text,
                                   insertion_order=self.event_counter)
        self.event_counter += 1

    def addProgramChange(self, tracknum, channel, time, program):
        if self.header.numeric_format == 1:
            tracknum += 1
        self.tracks[tracknum].addProgramChange(channel, self.time_to_ticks(time), program,
                                               insertion_order=self.event_counter)
        self.event_counter += 1

    def addChannelPressure(self, tracknum, channel, time, pressure_value):
        if self.header.numeric_format == 1:
            tracknum += 1
        track = self.tracks[tracknum]
        track.addChannelPressure(channel, self.time_to_ticks(time), pressure_value,
                                 insertion_order=self.event_counter)
        self.event_counter += 1

    def addControllerEvent(self, track, channel, time, controller_number,
                           parameter):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addControllerEvent(channel, self.time_to_ticks(time), controller_number,
                                              parameter, insertion_order=self.event_counter)  
        self.event_counter += 1

    def addPitchWheelEvent(self, track, channel, time, pitchWheelValue):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addPitchWheelEvent(channel, self.time_to_ticks(time), pitchWheelValue,
                                              insertion_order=self.event_counter)
        self.event_counter += 1

    def makeRPNCall(self, track, channel, time, controller_msb, controller_lsb,
                    data_msb, data_lsb, time_order=False):
        tick = self.time_to_ticks(time)

        if self.header.numeric_format == 1:
            track += 1
        track = self.tracks[track]

        tick_incr = 1 if time_order else 0
        track.addControllerEvent(channel, tick, 101,  
                                 controller_msb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        track.addControllerEvent(channel, tick, 100,
                                 controller_lsb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        track.addControllerEvent(channel, tick, 6,
                                 data_msb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        if data_lsb is not None:
            track.addControllerEvent(channel, tick, 38,
                                     data_lsb, insertion_order=self.event_counter)  
            self.event_counter += 1

    def makeNRPNCall(self, track, channel, time, controller_msb,
                     controller_lsb, data_msb, data_lsb, time_order=False):
        tick = self.time_to_ticks(time)

        if self.header.numeric_format == 1:
            track += 1
        track = self.tracks[track]

        tick_incr = 1 if time_order else 0
        track.addControllerEvent(channel, tick, 99,
                                 controller_msb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        track.addControllerEvent(channel, tick, 98,
                                 controller_lsb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        track.addControllerEvent(channel, tick, 6,
                                 data_msb, insertion_order=self.event_counter)  
        self.event_counter += 1
        tick += tick_incr
        if data_lsb is not None:
            track.addControllerEvent(channel, tick, 38,
                                     data_lsb, insertion_order=self.event_counter)  
            self.event_counter += 1

    def changeTuningBank(self, track, channel, time, bank, time_order=False):
        self.makeRPNCall(track, channel, time, 0, 4, 0, bank,
                         time_order=time_order)

    def changeTuningProgram(self, track, channel, time, program,
                            time_order=False):
        self.makeRPNCall(track, channel, time, 0, 3, 0, program,
                         time_order=time_order)

    def changeNoteTuning(self, track, tunings, sysExChannel=0x7F,
                         realTime=True, tuningProgam=0):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].changeNoteTuning(tunings, sysExChannel, realTime,
                                            tuningProgam,
                                            insertion_order=self.event_counter)
        self.event_counter += 1

    def addSysEx(self, track, time, manID, payload):
        tick = self.time_to_ticks(time)
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addSysEx(tick, manID, payload,
                                    insertion_order=self.event_counter)
        self.event_counter += 1

    def addUniversalSysEx(self, track, time, code, subcode, payload,
                          sysExChannel=0x7F, realTime=False):
        tick = self.time_to_ticks(time)
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addUniversalSysEx(tick, code, subcode, payload,
                                             sysExChannel, realTime,
                                             insertion_order=self.event_counter)  
        self.event_counter += 1

    def writeFile(self, fileHandle):
        self.header.writeFile(fileHandle)
        self.close()
        for i in range(0, self.numTracks):
            self.tracks[i].writeTrack(fileHandle)

    def shiftTracks(self, offset=0):
        origin = 100000000
        tick_offset = self.time_to_ticks(offset)

        for track in self.tracks:
            if len(track.eventList) > 0:
                for event in track.eventList:
                    if event.tick < origin:
                        origin = event.tick

        for track in self.tracks:
            tempEventList = []
            for event in track.eventList:
                adjustedTick = event.tick - origin
                event.tick = adjustedTick + tick_offset
                tempEventList.append(event)

            track.eventList = tempEventList

    def close(self):
        if self.closed: return
        for i in range(0, self.numTracks):
            self.tracks[i].closeTrack()
            self.tracks[i].MIDIEventList.sort(key=sort_events)

        origin = self.findOrigin()
        for i in range(0, self.numTracks):
            self.tracks[i].adjustTimeAndOrigin(origin, self.adjust_origin)
            self.tracks[i].writeMIDIStream()

        self.closed = True

    def findOrigin(self):
        origin = 100000000
        for track in self.tracks:
            if len(track.MIDIEventList) > 0:
                if track.MIDIEventList[0].tick < origin:
                    origin = track.MIDIEventList[0].tick

        return origin
