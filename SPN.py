# A S-P-N Assigment, implemented by following 
# 10/3/2021 
# Made BY Mahmoud Bargash and Mohamed Abohelal

from os import stat_result
import random
import hashlib


# 1- Create a sbox an its inverse
#sbox =     {0:0xE, 1:0x4, 2:0xD, 3:0x1, 4:0x2, 5:0xF, 6:0xB, 7:0x8, 8:0x3, 9:0xA, 0xA:0x6, 0xB:0xC, 0xC:0x5, 0xD:0x9, 0xE:0x0, 0xF:0x7} #key:value
#sbox_inv = {0xE:0, 0x4:1, 0xD:2, 0x1:3, 0x2:4, 0xF:5, 0xB:6, 0x8:7, 0x3:8, 0xA:9, 0x6:0xA, 0xC:0xB, 0x5:0xC, 0x9:0xD, 0x0:0xE, 0x7:0xF}

sbox =     {0:0x2, 1:0x1, 2:0xE, 3:0x7, 4:0x4, 5:0xa, 6:0x8, 7:0xD, 8:0xf, 9:0xc, 0xA:0x9, 0xB:0x0, 0xC:0x3, 0xD:0x5, 0xE:0x6, 0xF:0xb} #key:value
sbox_inv = {0x2:0, 0x1:1, 0xE:2, 0x7:3, 0x4:4, 0xa:5, 0x8:6, 0xD:7, 0xf:8, 0xc:9, 0x9:0xA, 0x0:0xB, 0x3:0xC, 0x5:0xD, 0x6:0xE, 0xb:0xF}


# -substitution and return the result
def substitution(Data, sbox):
    U_1_4 = [Data&0x000f, (Data&0x00f0)>>4, (Data&0x0f00)>>8, (Data&0xf000)>>12]
    result = 0
#    print ('S-P-N  Data = {:}'.format(U_1_4))
    for idx,u in enumerate(U_1_4):
        U_1_4[idx] = sbox[u]
        result = result| (U_1_4[idx] << 4*idx)
#    print ('S-P-N  result = {:}'.format(U_1_4))
    return result
    

# 2- Permutation
pbox = {0:0, 1:4, 2:8, 3:12, 4:1, 5:5, 6:9, 7:13, 8:2, 9:6, 10:10, 11:14, 12:3, 13:7, 14:11, 15:15}

# 3- Genrate keys K1-K5 
def keyGeneration():
    #k = hashlib.sha1( hex(random.getrandbits(128)).encode('utf-8') ).hexdigest()[2:2+20]
    #k='ffffffffffffffffffff'
    k='77777777777777777777'
    print(k)
    return k

# encrypt of S-P-N 
def encrypt(data, key):
    
    #create array of subkeys
    subKeys = [ int(subK,16) for subK in [ key[0:4],key[4:8], key[8:12], key[12:16], key[16:20] ] ]
    for round in range(0,3):
    
        # bit-wise exclusive-OR between the key bits associated with a round (referred to as a subkey)
        data = data^subKeys[round]
        
        # substitution and return the result
        data = substitution(data,sbox)
        
        # Permutation
        temp = 0      
        for i in range(0,16):
            if(data & (1 << i)):
                temp |= (1 << pbox[i])
        data = temp
    
    # Last round of S-P-N 
    data = data^subKeys[3] 
    data = substitution(data,sbox)
    data = data^subKeys[4] 
    
    return data


if __name__ == "__main__":
    
    # Generate the keys
    keys = keyGeneration()
    print(keys)
    # Generate a file Of Plain text Data + its chipher
    fileOfData = 'testData/' + keys[0:20] + '.dat'
    nOfSamples = 10000
    file = open(fileOfData,"w")
    print ('S-P-N  with key K = {:}'.format(keys))
    
    for sample in range(0, nOfSamples):     
        file.write('{:04x}, {:04x}\n'.format(sample, encrypt(sample, keys)))
    
    file.close()
    
    print ('{:} encrypted .'.format(nOfSamples))
    
                 
