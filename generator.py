import os

os.system('cls')

# import random
# choices = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
# key = "c3376601"
# for i in range(64-8):
#     key+=str(random.choice(choices))
# print(key)

plaintext = b'I wonder how many letters I have to work with? Heaps. Very good.'

text = bytearray(plaintext)
print(text)