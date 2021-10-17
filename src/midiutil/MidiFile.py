from Helper import sortEvents
from MIDIHeader import MIDIHeader
from MIDITrack import MIDITrack

controllerEventTypes = {'pan': 0x0a}
QUARTER_NOTE_TICKS = 960
MAJOR = 0
MINOR = 1
SHARPS = 1
FLATS = -1

class MIDIFile(object):
    def __init__(
            self, 
            numTracks=1, 
            removeDuplicates=True, 
            deinterleave=True, 
            adjustOrigin=False, 
            fileFormat=1, 
            quarterNoteTicks=QUARTER_NOTE_TICKS, 
            isEventTimeTicks=False
        ):
        self.header = MIDIHeader(self.numTracks, fileFormat, quarterNoteTicks)
        self.tracks = []
        self.numTracks = numTracks + 1 if fileFormat == 1 else self.numTracks = numTracks
        self.adjustOrigin = adjustOrigin
        self.isClosed = False
        self.quarterNoteTicks = quarterNoteTicks
        self.isEventTimeTicks = isEventTimeTicks
        self.convertTimeToTicks = lambda x: x if self.isEventTimeTicks else self.convertTimeToTicks = self.convertQuarterToTicks

        for i in range(0, self.numTracks):
            self.tracks.append(MIDITrack(removeDuplicates, deinterleave))
        self.event_counter = 0

    def convertQuarterToTicks(self, quarterNoteTime):
        return int(quarterNoteTime * self.quarterNoteTicks)

    def getNumberOfQuarterNotes(self, ticks):
        return float(ticks) / self.quarterNoteTicks

    def addNote(self, track, channel, pitch, time, duration, volume, annotation=None):
        if self.header.numeric_format == 1: track += 1
        self.tracks[track].addNoteByNumber(channel, pitch, self.convertTimeToTicks(time), self.convertTimeToTicks(duration), volume, annotation=annotation, insertion_order=self.event_counter)
        self.event_counter += 1

    def addTrackName(self, track, time, trackName):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addTrackName(self.convertTimeToTicks(time), trackName, insertion_order=self.event_counter)
        self.event_counter += 1

    def addTimeSignature(self, track, time, numerator, denominator, clocks_per_tick, notes_per_quarter=8):
        if self.header.numeric_format == 1:
            track = 0

        self.tracks[track].addTimeSignature(self.convertTimeToTicks(time), numerator, denominator, clocks_per_tick, notes_per_quarter, insertion_order=self.event_counter)
        self.event_counter += 1

    def addTempo(self, track, time, tempo):
        if self.header.numeric_format == 1:
            track = 0
        self.tracks[track].addTempo(self.convertTimeToTicks(time), tempo,
                                    insertion_order=self.event_counter)
        self.event_counter += 1

    def addCopyright(self, track, time, notice):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addCopyright(self.convertTimeToTicks(time), notice,
                                        insertion_order=self.event_counter)
        self.event_counter += 1

    def addKeySignature(self, track, time, accidentals, accidental_type, mode,
                        insertion_order=0):
        if self.header.numeric_format == 1:
            track = 0  
        self.tracks[track].addKeySignature(self.convertTimeToTicks(time), accidentals, accidental_type,
                                           mode, insertion_order=self.event_counter)
        self.event_counter += 1

    def addText(self, track, time, text):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addText(self.convertTimeToTicks(time), text,
                                   insertion_order=self.event_counter)
        self.event_counter += 1

    def addProgramChange(self, tracknum, channel, time, program):
        if self.header.numeric_format == 1:
            tracknum += 1
        self.tracks[tracknum].addProgramChange(channel, self.convertTimeToTicks(time), program,
                                               insertion_order=self.event_counter)
        self.event_counter += 1

    def addChannelPressure(self, tracknum, channel, time, pressure_value):
        if self.header.numeric_format == 1:
            tracknum += 1
        track = self.tracks[tracknum]
        track.addChannelPressure(channel, self.convertTimeToTicks(time), pressure_value,
                                 insertion_order=self.event_counter)
        self.event_counter += 1

    def addControllerEvent(self, track, channel, time, controller_number,
                           parameter):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addControllerEvent(channel, self.convertTimeToTicks(time), controller_number,
                                              parameter, insertion_order=self.event_counter)  
        self.event_counter += 1

    def addPitchWheelEvent(self, track, channel, time, pitchWheelValue):
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addPitchWheelEvent(channel, self.convertTimeToTicks(time), pitchWheelValue,
                                              insertion_order=self.event_counter)
        self.event_counter += 1

    def makeRPNCall(self, track, channel, time, controller_msb, controller_lsb,
                    data_msb, data_lsb, time_order=False):
        tick = self.convertTimeToTicks(time)

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
        tick = self.convertTimeToTicks(time)

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
        tick = self.convertTimeToTicks(time)
        if self.header.numeric_format == 1:
            track += 1
        self.tracks[track].addSysEx(tick, manID, payload,
                                    insertion_order=self.event_counter)
        self.event_counter += 1

    def addUniversalSysEx(self, track, time, code, subcode, payload,
                          sysExChannel=0x7F, realTime=False):
        tick = self.convertTimeToTicks(time)
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
        tickOffset = self.convertTimeToTicks(offset)

        for track in self.tracks:
            if len(track.eventList) > 0:
                for event in track.eventList:
                    if event.tick < origin:
                        origin = event.tick

        for track in self.tracks:
            tempEventList = []
            for event in track.eventList:
                adjustedTick = event.tick - origin
                event.tick = adjustedTick + tickOffset
                tempEventList.append(event)

            track.eventList = tempEventList

    def close(self):
        if self.isClosed: return
        for i in range(0, self.numTracks):
            self.tracks[i].closeTrack()
            self.tracks[i].MIDIEventList.sort(key=sortEvents)

        origin = self.findOrigin()
        for i in range(0, self.numTracks):
            self.tracks[i].adjustTimeAndOrigin(origin, self.adjustOrigin)
            self.tracks[i].writeMIDIStream()

        self.isClosed = True

    def findOrigin(self):
        origin = 100000000
        for track in self.tracks:
            if len(track.MIDIEventList) > 0:
                if track.MIDIEventList[0].tick < origin:
                    origin = track.MIDIEventList[0].tick

        return origin
