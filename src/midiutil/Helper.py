import math
import struct


def writeVarLength(i):
    if i == 0: return [0]
    vlBytes = []
    hiBit = 0x00
    while i > 0:
        vlBytes.append(((i & 0x7f) | hiBit) & 0xff)
        i >>= 7
        hiBit = 0x80
    vlBytes.reverse()
    return vlBytes

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


def frequencyToBytes(frequency):
    resolution = 16384
    frequency = float(frequency)
    dollars = 69 + 12 * math.log(frequency / (float(440)), 2)
    firstByte = int(dollars)
    lowerFreq = 440 * pow(2.0, ((float(firstByte) - 69.0) / 12.0))
    centDif = 1200 * math.log((frequency / lowerFreq), 2) if frequency != lowerFreq else 0
    cents = round(centDif / 100 * resolution)
    secondByte = min([int(cents) >> 7, 0x7F])
    thirdByte = cents - (secondByte << 7)
    thirdByte = min([thirdByte, 0x7f])
    if thirdByte == 0x7f and secondByte == 0x7F and firstByte == 0x7F:
        thirdByte = 0x7e
    thirdByte = int(thirdByte)
    return [firstByte, secondByte, thirdByte]


def bytesToFrequency(bytes):
    resolution = 16384.0
    baseFrequency = 440 * pow(2.0, (float(bytes[0] - 69.0) / 12.0))
    frac = (float((int(bytes[1]) << 7) + int(bytes[2])) * 100.0) / resolution
    frequency = baseFrequency * pow(2.0, frac / 1200.0)
    return frequency


def sortEvents(event):
    return (event.tick, event.sec_sort_order, event.insertion_order)
