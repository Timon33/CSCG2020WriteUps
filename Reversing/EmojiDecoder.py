# Script that takes code.bin as an input and
# decodes the emoji instruction in it to
# assembly like instructions and writes them
# to a output file

import sys

emojiToInsruction = {
    b'\xf0\x9f\x92\xaa': "PUSH", #arm
    b'\xF0\x9F\x93\x96': "READ", #book
    b'\xe2\x9c\x8f\xef\xb8\x8f': "WRITE", #pen
    b'\xf0\x9f\xa6\xbe': "LD08", #mech arm
    b'\xf0\x9f\x94\x80': "XOR", #swich arrow
    b'\xe2\x9c\x85': "OR", #tick
    b'\xf0\x9f\xa4\x94': "JMP", #thinking face
    b'\xf0\x9f\x92\x80': "EXIT", #skull
    b'\xf0\x9f\x8c\xa0': "LD32", #falling star
    b'\xe2\x80\xbc\xef\xb8\x8f': "COPY", #douple exclamation
    b'\xe2\x9e\x95': "AND    0x1", #cross
    b'\xe2\x9e\xa1\xef\xb8\x8f': "SHR" #arrow
}

def HasParameter(symbol):
    code = emojiToInsruction[symbol]
    if (code == "PUSH") | (code[:2] == "LD") | (code == "JMP") | (code == "SHR"):
        return True
    return False

def UTF8decodeInt(byte):
    if (byte & 0xf0) == 0xf0:
        return 4
    elif (byte & 0xe0) == 0xe0:
        return 3
    elif (byte & 0xc0) == 0xc0:
        return 2
    elif (byte & 0x80) == 0:
        return 1
    else:
        print("ERROR can find decode int for {}".format(byte))

def NumberEmojisToInt(bytes):
    integers = []
    offset = 0
    for i in range(6):
        integers.append(int(chr(bytes[offset])))
        offset += 1
        offset += UTF8decodeInt(bytes[offset])
        offset += UTF8decodeInt(bytes[offset])

    result = 0
    for i in range(3):
        result += integers[i*2+1] ** integers[i*2]

    return offset, result

def GetNextEmoji(offset, code):
    len = UTF8decodeInt(code[offset])
    newOffset = len + offset
    symbol = code[offset:newOffset]
    return newOffset, symbol

def Decode(code, file):
    offset = 0
    while offset < len(code):
        s = "{0:04X} - ".format(offset)
        offset, symbol = GetNextEmoji(offset, code)

        try:
            s += emojiToInsruction[symbol]
        except KeyError:
            #maybe it's 2 utf-8 chars
            offset, sym = GetNextEmoji(offset, code)
            symbol += sym
            try:
                s += emojiToInsruction[symbol]
            except KeyError: #cant be 3 so it's a error
                print("ERROR: {0} not found in instructions. offset {1}".format(symbol, offset))
                return
        #if it has number emojis turn them to int and append
        if HasParameter(symbol):
            os, parameter = NumberEmojisToInt(code[offset:])
            offset += os
            s += "\t {0:04X}".format(parameter)

            op = emojiToInsruction[symbol]
            if  op == "JMP":
                s += "\t({0:04X})".format(parameter + offset)
            elif op[:2] == "LD":
                lad = int.from_bytes(seg1[parameter:parameter + int(op[2:])], byteorder='big')
                s += "\t({0:04X})".format(lad)

        s += "\n"
        file.write(s)
        #print(hex(offset))

if len(sys.argv) < 3:
    print("USAGE: EmojiDecoder.py <code.bin> <outputFile>")
    exit()

try:
    code = open(sys.argv[1], "rb")
except FileNotFoundError:
    print("ERROR: file {0} not found".format(sys.argv[1]))

try:
    output = open(sys.argv[2], 'w')
except FileNotFoundError:
    print("ERROR: file {0} not found".format(sys.argv[2]))

seg1 = code.read(0x200)
code.seek(0x200)
buf = code.read()
print(buf[:100])
code.close()


Decode(buf, output)

output.close()
