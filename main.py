import os
import random

from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_ECB, MODE_CTR
from convert import BinaryToHex, StringToBinary, HexToBinary

os.system('cls')

random.seed(1)

def printNonce(nonce):
    for i in nonce:
        binary = "{:08d}".format(int(bin(i).split('b')[1]))
        print(BinaryToHex(binary),end="")
    print("")

def ByteToBit(arr):
    bits = ""
    for i in arr:
        bits += "{:08d}".format(int(bin(i).split("b")[1]))
    return bits

def XOR(outNonce, chunk):
    outNonceBits = ByteToBit(outNonce)
    chunkBits = ByteToBit(chunk)
    result = ""
    for i in range(len(chunkBits)):
        if outNonceBits[i] != chunkBits[i]:
            result += str(1)
        else:
            result += str(0)
    # print(outNonceBits)
    # print(chunkBits)
    # print(result)
    return result

# 256-bit key (32 bytes)
# Storing as a hexadecimal number, but need to convert to string and then encode as bytes
# Size of key is 64 characters * 4 bits = 256 bits (32 bytes)
hex_key = 'C3376601427A45DBD2AD34DBCD5325E25E0305F48B3A9A3FCB80E861858AB249'
byte_key = bytearray.fromhex(hex_key)

# 512-bit plaintext (64 bytes)
plaintext = "I wonder how many letters I have to work with? Heaps. Very good."
byte_plaintext = bytearray(plaintext.encode())

# Create a nonce randomly
# Size of nonce is 8 bits * 16 = 128 bits (16 bytes)
nonce_length = 16
temp_array = []
for i in range(nonce_length):
    temp_array.append(random.randint(0,255))
nonce = bytearray(temp_array)

print("Entire Plaintext:", StringToBinary(plaintext))
print("Key:", HexToBinary(hex_key))
print("IV:", ByteToBit(nonce))

# Define cipher
cipher = AES.new(key=byte_key, mode=MODE_ECB)

# print(len(byte_key)*8)
# print(len(plaintext)*8)
# print(len(nonce)*8)

ciphertext = ""
counter = 1
for i in range(0, len(byte_plaintext), len(nonce)):
    print("\nBlock ", counter, ":", sep="")
    print("    Input of AES:", ByteToBit(nonce))
    outNonce = cipher.encrypt(nonce)
    print("    Output of AES:", ByteToBit(outNonce))
    chunk = byte_plaintext[i:i+len(nonce)]
    # print(chunk)
    result = XOR(outNonce, chunk)
    print("    Result of XOR:", result)
    ciphertext += result
    nonce[-1]+=1

print("\nEntire Ciphertext:", ciphertext)

# plaintext = "A good Plaintext"
# print(StringToBinary(plaintext))
# print(len(StringToBinary(plaintext)))

# cipher = AES.new(key=byte_key, mode=MODE_ECB)

