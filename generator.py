import random
choices = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
key = "c3376601"
for i in range(64-8):
    key+=str(random.choice(choices))
print(key)