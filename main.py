import os
import random

from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_ECB
from convert import BinaryToHex, StringToBinary, HexToBinary, StringToHex

os.system('cls')

random.seed(1)

def printIV(iv):
    for i in iv:
        binary = "{:08d}".format(int(bin(i).split('b')[1]))
        print(BinaryToHex(binary),end="")
    print("")

def nicePrintBits(byteString):
    for i in range(0,len(byteString), 8):
        print(byteString[i:i+8],end=" ")
    print("")

def ByteToBit(arr):
    bits = ""
    for i in arr:
        bits += "{:08d}".format(int(bin(i).split("b")[1]))
    return bits

def XOR(outIV, chunk):
    outIVBits = ByteToBit(outIV)
    chunkBits = ByteToBit(chunk)
    result = ""
    for i in range(len(chunkBits)):
        if outIVBits[i] != chunkBits[i]:
            result += str(1)
        else:
            result += str(0)
    return result

def compareCipher(ciphertext1, ciphertext2):
    differences = 0
    difference_positions = ""
    for j in range(len(ciphertext1)):
        if ciphertext1[j] != ciphertext2[j]:
            differences+=1
            difference_positions+=u'\u2193'
        else:
            difference_positions+=" "
        if (j+1)%8==0:
            difference_positions+=" "
    print("Number of altered bits ",counter, " = ",differences,sep="")

# 256-bit key (32 bytes)
# Storing as a hexadecimal number, but need to convert to string and then encode as bytes
# Size of key is 64 characters * 4 bits = 256 bits (32 bytes)
hex_key = 'c3376601427a45dbd2ad34dbcd5325e25e0305f48b3a9a3fcb80e861858ab249'
byte_key = bytearray.fromhex(hex_key)

# 512-bit plaintext (64 bytes)
plaintext = "I wonder how many letters I have to work with? Heaps. Very good."
byte_plaintext = bytearray(plaintext.encode())

# Create a nonce randomly
# Size of nonce is 8 bits * 16 = 128 bits (16 bytes)
nonce_length = 16
nonce_array = []
for i in range(nonce_length):
    nonce_array.append(random.randint(0,255))
iv = bytearray(nonce_array)

print("Entire Plaintext:", StringToHex(plaintext))
print("Key:", hex_key)
print("IV:", BinaryToHex(ByteToBit(iv)))

# Define cipher
cipher = AES.new(key=byte_key, mode=MODE_ECB)

ciphertext = ""
counter = 1
for i in range(0, len(byte_plaintext), len(iv)):
    print("\nBlock ", counter, ":", sep="")
    print("    Input of AES: ", BinaryToHex(ByteToBit(iv)))
    outIV = cipher.encrypt(iv)
    print("    Output of AES:", BinaryToHex(ByteToBit(outIV)))
    chunk = byte_plaintext[i:i+len(iv)]
    # print(chunk)
    result = XOR(outIV, chunk)
    print("    Result of XOR:", BinaryToHex(result))
    ciphertext += result
    iv[-1]+=1
    counter+=1

print("\nEntire Ciphertext:", BinaryToHex(ciphertext),"\n\n")


# five unique 1-bit flips
plaintext = "A good Plaintext"
byte_plaintext = bytearray(plaintext.encode())

# nicePrintBits(ByteToBit(byte_plaintext))

cipher = AES.new(key=byte_key, mode=MODE_ECB)

original_ciphertext = ByteToBit(cipher.encrypt(byte_plaintext))

ciphertext_list = []
swap_position = 0
counter = 1
for j in range(5):
    new_plaintext = ""
    for i in range(0,len(ByteToBit(byte_plaintext))):
        if (i == swap_position):
            if (ByteToBit(byte_plaintext)[i] == "0"):
                new_plaintext += "1"
            else:
                new_plaintext += "0"
        else:
            new_plaintext += ByteToBit(byte_plaintext)[i]
    print("1-bit flip ", counter,sep="")
    print("Original Plaintext: ",end="")
    nicePrintBits(ByteToBit(byte_plaintext))
    print("Swap Index =",swap_position,":    ", end="") 
    for i in range(swap_position+int(swap_position/8)):
        print(" ",end="")
    print(u'\u2193')
    swap_position += int(len(ByteToBit(byte_plaintext))/5)
    print("Altered Plaintext:  ",end="")
    nicePrintBits(new_plaintext)
    new_byte_plaintext = bytearray.fromhex(BinaryToHex(new_plaintext))
    ciphertext = cipher.encrypt(new_byte_plaintext)
    #nicePrintBits(ByteToBit(ciphertext))
    print("")
    ciphertext_list.append(ByteToBit(ciphertext))
    counter+=1

ciphertext = cipher.encrypt(byte_plaintext)

print("")
counter = 1
for variant_ciphertext in ciphertext_list:
    differences = 0
    difference_positions = ""
    for j in range(len(variant_ciphertext)):
        if original_ciphertext[j] != variant_ciphertext[j]:
            differences+=1
            difference_positions+=u'\u2193'
        else:
            difference_positions+=" "
        if (j+1)%8==0:
            difference_positions+=" "
    print("Number of altered bits ",counter, " = ",differences,sep="")
    print("Original Ciphertext:  ", end="")
    nicePrintBits(original_ciphertext)
    print("Difference Positions: ", end="")
    print(difference_positions)
    print("Altered Ciphertext:   ", end="")
    nicePrintBits(variant_ciphertext)
    print("")
    counter+=1