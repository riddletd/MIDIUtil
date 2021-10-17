import math
import struct


def writeVarLength(i):
    if i == 0: return [0]
    bytes = []
    hiBit = 0x00
    while i > 0:
        bytes.append(((i & 0x7f) | hiBit) & 0xff)
        i >>= 7
        hiBit = 0x80
    bytes.reverse()
    return bytes

def readVarLength(offset, buffer):
    tickOffset = offset
    output = 0
    bytesRead = 0
    while True:
        output = output << 7
        byte = struct.unpack_from('>B', buffer, tickOffset)[0]
        tickOffset = tickOffset + 1
        bytesRead = bytesRead + 1
        output = output + (byte & 127)
        if (byte & 128) == 0:
            break
    return (output, bytesRead)


def frequencyToBytes(frequency: float):
    RESOLUTION = 16384
    firstByte = int(getDollars(frequency))
    secondByte = min([int(getCents(RESOLUTION, getCentDifference(frequency, getLowFrequency(firstByte)))) >> 7, 0x7F])
    thirdByte = min([getCents(RESOLUTION, getCentDifference(frequency, getLowFrequency(firstByte))) - (secondByte << 7), 0x7f])
    if thirdByte == 0x7f and secondByte == 0x7F and firstByte == 0x7F: thirdByte = 0x7e
    return [firstByte, secondByte, int(thirdByte)]

def getDollars(frequency: float):
    return 69 + 12 * math.log(frequency / (float(440)), 2)

def getLowFrequency(firstByte: int):
    return 440 * pow(2.0, ((float(firstByte) - 69.0) / 12.0))

def getCentDifference(frequency: float, lowerFreq: float):
    return 1200 * math.log((frequency / lowerFreq), 2) if frequency != lowerFreq else 0

def getCents(resolution, centDif):
    return round(centDif / 100 * resolution)

def bytesToFrequency(bytes):
    resolution = 16384.0
    baseFrequency = 440 * pow(2.0, (float(bytes[0] - 69.0) / 12.0))
    frac = (float((int(bytes[1]) << 7) + int(bytes[2])) * 100.0) / resolution
    frequency = baseFrequency * pow(2.0, frac / 1200.0)
    return frequency

def sortEvents(event):
    return (event.tick, event.sec_sort_order, event.insertion_order)
