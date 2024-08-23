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

def compareCiphertext(ciphertext1, ciphertext2):
    differences = 0
    for i in range(len(ciphertext1)):
        if ciphertext1[i] != ciphertext2[i]:
            differences+=1
    return differences

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


##########################################
##########################################
##########################################

cipher = AES.new(key=byte_key, mode=MODE_ECB)

plaintext_original = bytearray("A Good Plaintext".encode())
ciphertext_original = ByteToBit(cipher.encrypt(plaintext_original))

ciphertext_variants = [ciphertext_original]
swap_index = 0
counter = 1
for j in range(5):
    # Copy the original plaintext, flipping a single bit at the swap position index
    plaintext_variant = ""
    for i in range(0,len(ByteToBit(plaintext_original))):
        if (i == swap_index):
            if (ByteToBit(plaintext_original)[i] == "0"):
                plaintext_variant += "1"
            else:
                plaintext_variant += "0"
        else:
            plaintext_variant += ByteToBit(plaintext_original)[i]

    # Print header information
    print("Bit Flip ", counter,sep="")

    # Print original plaintext
    print("Original Plaintext: ",end="")
    nicePrintBits(ByteToBit(plaintext_original))

    # Print arrows indicating bit flip location
    print("Swap Index = ",swap_index,":    ", end="",sep="") 
    for i in range(swap_index+int(swap_index/8)):
        print(" ",end="")
    if (len(str(swap_index)) == 1):
        print(" ",end="")
    print(u'\u2193')

    # Print altered plaintext
    print("Altered Plaintext:  ",end="")
    nicePrintBits(plaintext_variant)
    print("")

    # Create the altered plaintext's associated ciphertext and save to array
    ciphertext_variant = cipher.encrypt(bytearray.fromhex(BinaryToHex(plaintext_variant)))
    ciphertext_variants.append(ByteToBit(ciphertext_variant))

    # Increment required variables
    swap_index += int(len(ByteToBit(plaintext_original))/5)
    counter += 1

# Print out specific example of ciphertext avalanche analysis
print("\nCiphertext Variant 4: ", end="")
nicePrintBits(ciphertext_variants[4])
print("Difference Arrows:    ", end="")
differences = 0
for i in range(len(ciphertext_variants[4])):
    if ciphertext_variants[4][i] != ciphertext_variants[5][i]:
        differences+=1
        print(u"\u2193", end="")
    else:
        print(" ", end="")
    if ((i+1)%8 == 0):
        print(" ",end="")
print("")
print("Ciphertext Variant 5: ", end="")
nicePrintBits(ciphertext_variants[5])
print("\nTotal Differences =", differences)
print("Percentage Difference = ", "{:5.2f}".format((differences/len(ciphertext_variants[4]))*100), "%", sep="")

# Print out difference table
print("\n\n   |  ", end="")
for i in range(len(ciphertext_variants)):
    print(" C", i, "   |  ", end="", sep="")
print("")

for i in range(len(ciphertext_variants)):
    print("C", i, end=" | ", sep="")
    for j in range(len(ciphertext_variants)):
        differences = compareCiphertext(ciphertext_variants[i], ciphertext_variants[j])
        print("{:5.2f}".format(differences/len(ciphertext_variants[i])*100), "%", sep="", end=" | ")
    print("")