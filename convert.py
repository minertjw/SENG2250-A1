# Number System Converters
def StringToHex(text_string):
    hex_string = ''
    for t in text_string:
        hex_string += hex(ord(t)).split('x')[1]
    return hex_string

def StringToBinary(text_string):
    binary_string = ''
    for t in text_string:
        byte = bin(ord(t)).split('b')[1]
        while len(byte) < 8:
            byte = "0"+byte
        binary_string += byte
    return binary_string

def HexToString(hex_string):
    text_string = ''
    for i in range(0,len(hex_string),2):
        text_string += chr(int(hex_string[i]+hex_string[i+1],16))
    return text_string

def HexToBinary(hex_string):
    binary_string = ''
    for element in hex_string:
        nibble = bin(int(element,16)).split('b')[1]
        while len(nibble) < 4:
            nibble = '0'+nibble
        binary_string += nibble
    return binary_string

def BinaryToString(binary_string):
    text_string = ''
    for i in range(0, len(binary_string), 8):
        text_string += chr(int(binary_string[i:i+8],2))
    return text_string

def BinaryToHex(binary_string):
    hex_string = ''
    for i in range(0, len(binary_string), 4):
        hex_string += hex(int(binary_string[i:i+4],2)).split('x')[1]
    return hex_string
