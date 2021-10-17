import struct


class MIDIHeader(object):
    def __init__(self, numTracks, file_format, ticks_per_quarternote):
        self.headerString = struct.pack('cccc', b'M', b'T', b'h', b'd')
        self.headerSize = struct.pack('>L', 6)
        self.formatnum = struct.pack('>H', file_format)
        self.numeric_format = file_format
        self.numTracks = struct.pack('>H', numTracks)
        self.ticks_per_quarternote = struct.pack('>H', ticks_per_quarternote)

    def writeFile(self, fileHandle):
        fileHandle.write(self.headerString)
        fileHandle.write(self.headerSize)
        fileHandle.write(self.formatnum)
        fileHandle.write(self.numTracks)
        fileHandle.write(self.ticks_per_quarternote)
