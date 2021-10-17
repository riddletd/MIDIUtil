from midiutil import MIDIFile

MyMIDI = MIDIFile(1)
track = 0
time = 0
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)
channel = 0
pitch = 60
duration = 1
volume = 100

MyMIDI.addNote(track, channel, pitch, time, duration, volume)

with open("output.mid", 'wb') as binfile:
    MyMIDI.writeFile(binfile)
