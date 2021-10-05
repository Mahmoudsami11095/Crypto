# A S-P-N Linear Crypto_analysis Assigment, implemented by following 
# 10/3/2021 
# Made BY Mahmoud Bargash and Mohamed Abohelal

import SPN
from math import trunc, fabs
import itertools as it
import collections   

# Build table of input values
sbox_in = ["".join(seq) for seq in it.product("01", repeat=4)]
print(sbox_in)  
# Build a table of output values
sbox_out = [ bin(SPN.sbox[int(seq,2)])[2:].zfill(4) for seq in sbox_in ]
print(sbox_out)
# Build an ordered dictionary between input and output values
sbox_b = collections.OrderedDict(zip(sbox_in,sbox_out))
print(sbox_b)
# Create the Linear Approximation Table (LAT)
probBias = [[0 for x in range(len(sbox_b))] for y in range(len(sbox_b))] 

# Linear Approximation Table
print('Linear Approximation Table: ')
for bits in sbox_b.items():
    input_bits, output_bits = bits
    X1,X2,X3,X4 = [ int(bits,2) for bits in [input_bits[0],input_bits[1],input_bits[2],input_bits[3]] ]
    Y1,Y2,Y3,Y4 = [ int(bits,2) for bits in [output_bits[0],output_bits[1],output_bits[2],output_bits[3]] ]
                
    inputs = [0, X4, X3, X3^X4, X2, X2^X4, X2^X3, X2^X3^X4, X1, X1^X4,
                    X1^X3, X1^X3^X4, X1^X2, X1^X2^X4, X1^X2^X3, X1^X2^X3^X4] 
                    
    outputs = [0, Y4, Y3, Y3^Y4, Y2, Y2^Y4, Y2^Y3, Y2^Y3^Y4, Y1, Y1^Y4,
                    Y1^Y3, Y1^Y3^Y4, Y1^Y2, Y1^Y2^Y4, Y1^Y2^Y3, Y1^Y2^Y3^Y4]                
    
    for input in range (0, len(inputs)):
        for output in range (0, len(outputs)):
            probBias[input][output] += (inputs[input]==outputs[output])

# Print the LAT
for bias in probBias:
    for bia in bias:
        print('{:d}'.format(bia-8).zfill(2), end=' ')
    print('')
    

# Create array of for counting bias
cntSubKeyBias = [0]*256

# Open the File of the generated Data(Plain-text_Cipher) 
file1 = open('testData/myfile.txt', 'r')
Lines = file1.readlines()

for line in Lines:
    # Read Data(Plain-text)
    Plain_Text = int(line.split(",")[0].strip(),16)
    # Read Data(Cipher)
    Cipher = int(line.split(",")[1].strip(),16)
    # Read the byte of Data(Cipher) that we will use to get the partial key
    Cipher_5_8  = (Cipher>>8) & 0xF
    Cipher_9_12 = (Cipher>>4) & 0xF
    
    # Try all possible of the Partial key
    for pKey in range(256):
        pKey_5_8  = (pKey>>4) & 0xF
        pKey_9_12 = (pKey)    & 0xF
        v_5_8  = (Cipher_5_8  ^ pKey_5_8)
        v_9_12 = (Cipher_9_12 ^ pKey_9_12)
       
	    # Get U to use it in the Equation
        u_5_8, u_9_12 = SPN.sbox_inv[v_5_8], SPN.sbox_inv[v_9_12]
        
	    # linear approximation equation ==> U_{4,6}⊕U_{4,7}⊕U_{4,10}⊕U_{4,11}⊕P_{5}⊕P_{9}⊕P_{10}
        eq_LA = ((u_5_8>>2)&0b1)^((u_5_8>>1)&0b1)^((u_9_12>>2)&0b1)^((u_9_12>>1)&0b1)^((Plain_Text>>6)&0b1)^((Plain_Text>>7)&0b1)
        if eq_LA == 0:
            cntSubKeyBias[pKey] += 1
	         
# Calculate the Bias of the 10000 sample
bias = [fabs(LA - 5000.0)/10000.0 for LA in cntSubKeyBias]

max_val, max_i = 0,0
for r_i, res in enumerate(bias):
    if res > max_val:
        max_val = res
        max_i = r_i

print('\nHighest bias is {:} for subKey value "{:}".'.format(max_val, hex(max_i)))



