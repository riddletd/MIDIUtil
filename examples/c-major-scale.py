#!/usr/bin/env python

from midiutil import MIDIFile

notes = [60, 62, 64, 65, 67, 69, 71, 72]
track = 0
channel = 0
time = 0
duration = 1
tempo = 60
volume = 100

MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(notes):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

for i, pitch in enumerate(notes):
    MyMIDI.addNote(track, channel, pitch + 3, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
