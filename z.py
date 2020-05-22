import numpy
import pickle

from x import Shape

stuff = pickle.load ( open ("wibble.in", "rb"), encoding='latin1')

print (stuff.keys())
print (len (stuff ['1']))
#print (stuff ['1'][0])

for i in range (len (stuff ['3'])):
    x= stuff ['3'][i].txlate ([0, 0, 1])
    if min ([j.min() for j in x.blox]) >= 0:
        #print (x.__str__())
        print (x.txlate ([0, 0, -1]).__str__())
        pass


z1 = Shape ([[0, 0, 0], [0, 0, 1], [0, 0, 2], [1, 0, 0], [1, 0, 1], [0, 1, 2]])
z2 = Shape ([[0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 2], [0, 2, 1], [1, 2, 1]])
z3 = Shape ([[0, 0, 2], [0, 0, 1], [0, 0, 0], [0, 1, 2], [0, 1, 1], [1, 0, 0]])
z  = Shape ([[0, 0, 0], [1, 0, 0], [1, 0, 1], [1, -1, 1], [1, 0, 2], [ 2, 0, 2]]) 
#[[ 2  0  1]\n [ 2 -1  1]\n [ 1  0  1]\n [ 1 -1  1]\n [ 0  0  1]\n [ 0  0  0]]
#[[0 0 2]\n [0 0 1]\n [0 0 0]\n [0 1 2]\n [0 1 1]\n [1, 0, 0]])
for a in stuff.keys ():
    for y in stuff [a]:
        if z.__cmp__(y): print ("z, a, y, z==y", z, a, y)

