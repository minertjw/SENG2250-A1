from Crypto.Cipher import AES
from convert import StringToHex, StringToBinary, BinaryToString, HexToString, BinaryToHex, HexToBinary
from Crypto.Util.Padding import pad

# 256-bit key (32 bytes)
key = HexToString("C33766014D61927FE7DCCECEAF5D8A2DA172A1EDF8A6CEAED9E39959273FABCD").encode()

print(type(key))

# 512-bit plaintext (64 bytes)
plaintext = b'I wonder how many letters I have to work with? Heaps. Very good.'

# Create AES cipher in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Pad the plaintext to be a multiple of the block size (16 bytes)
padded_plaintext = pad(plaintext, AES.block_size)

# Encrypt the plaintext
ciphertext = cipher.encrypt(padded_plaintext)

print(f'Ciphertext: {ciphertext.hex()}')
