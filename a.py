from x import Shape
import pickle


import re

x = re.compile (r"""\d\         # shape name to try
                  \[		# bracket around array of voids
                  ((\'\[( |\-)?\d\ ( |\-)?\d\ ( |\-)?\d\]\'(,\ )?)*)
                  \]
                  \ \[((\'\[
                    ((\[(\ |-)?\d\ (\ |-)?\d\ (\ |-)?\d\](\\n\ )?)*)\]\'(,\ )?)*)

""",
                 re.VERBOSE)

dl = re.compile (r"((\d){4,4}-.*)")
infile = open ("rr", "r")

l = infile.readline()
l = infile.readline ()
#
j =  x.search (l).groups ()

doneLocStr = x.search (l).group (1).split (",")
Locs = [i.strip ("' []") for i in doneLocStr]


def parseLoc (inStr):
    ret = []
    for x in inStr.split ():
        ret.append (int (x))
    return ret

x = parseLoc (Locs [0])

fillersStr = j[6].split (",")

def parseFiller (inStr):
    ret = []
    for x in inStr.split ("\\n"):
#        print "str", x
        ints = x.strip ("\'\[\] ").split ()
        ret.append ([int (i) for i in ints])
    return ret

jj = parseFiller (fillersStr [0])
z = Shape (jj)

stuff = pickle.load (open ("wibble.in", "r"))

for i in range (len (Locs)):
    x = parseLoc (Locs [i])
    jj = parseFiller (fillersStr [i])
    z = Shape (jj)


    for a in stuff.keys ():
        for y in stuff [a]:
            if z.__cmp__(y): print "x, z, a, z==y", x, z, a

for i in stuff ['0']:
    ok = True
    if min ([j.min () for j in i.txlate ([0,0,1]).blox]) >= 0:
        print i.__str__()

print len (stuff ['1'])
