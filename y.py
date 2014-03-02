import re
from numpy import *
a = open ("rub", "r").readlines ()
print a [0]
p = re.compile (r"\[\'(\d+)\', \'(\d+)\'\]")
for j in a:
    try:
        print p.findall (j)
#        print [ x.group () for x in p.findall (j)]
    except IndexError:
        print "failed", j
