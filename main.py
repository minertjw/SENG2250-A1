import os
import random
import json

from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_ECB, MODE_CTR
from base64 import b64encode, b64decode

os.system('cls' if os.name == 'nt' else 'clear')

random.seed(1)

# 256-bit key (32 bytes)
# Storing as a hexadecimal number, but need to convert to string and then encode as bytes
# Size of key is 64 characters * 4 bits = 256 bits (32 bytes)
hex_key = 'C3376601427A45DBD2AD34DBCD5325E25E0305F48B3A9A3FCB80E861858AB249'
byte_key = bytearray.fromhex(hex_key)

mode = MODE_ECB
mode = MODE_CTR

# Nonce length in bytes
nonce_length = 64

# Create a nonce randomly
temp_array = []
for i in range(nonce_length/8):
    temp_array.append(random.randint(0,255))
nonce = bytearray(temp_array)

initial_value = 0

# 512-bit plaintext (64 bytes)
plaintext = b'I wonder how many letters I have to work with? Heaps. Very good.'


cipher = AES.new(key=byte_key, mode=MODE_CTR, nonce=nonce, initial_value=initial_value, counter=None)

returned_nonce = cipher.nonce

ct_bytes = cipher.encrypt(plaintext)
nonce = b64encode(cipher.nonce).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'nonce':nonce, 'ciphertext':ct})
print(result)

try:
    cipher = AES.new(byte_key, MODE_CTR, nonce=b64decode(nonce))
    pt = cipher.decrypt(b64decode(ct))
    print("The message was:", pt)
except (ValueError, KeyError):
    print("Incorrect decryption")