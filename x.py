import unittest
import sys
import getopt
import numpy
import psyco
import pickle
import datetime


""" prog to solve the 4x4x4 cube that phil a gave me. staring with numpy for arrays """

# need class around this global variable
class Stuff ():
    stuff = {}

class Cube (object):

    def __init__ (self, size):
# create an empty array of the right size, then reshape it
        x = [False for y in range (size ** 3)]
        self.frame = numpy.array (x, dtype = bool)
#        print (self.frame)
        self.frame.shape = (size, size, size)
        self.blox = []
        self.size = size
        
    def filled (self):
        return len (self.blox)

    def __cmp__ (self, other):
# could put in try block, but easier just to check sizing first
        if self.size != other.size: return False
#        return numpy.all (self.spitEmOut () == other.spitEmOut ())
        s1 = self.spitEmOut ().tolist ()
        s2 = other.spitEmOut ().tolist ()
        s1.sort ()
        s2.sort ()
        return (s1 == s2)

# untested?
    def fill3 (self, x, y, z):
#        self.blox.append (numpy.array ([x, y, z]))
        a = numpy.array ([x, y, z])
        if self.has (a):
            return False
        else:
            self.blox.append (a)
            return True

    def fill (self, lst):
        assert 3 == len (lst), "wrong length of lst to fill: {}".format (len (lst))
#        self.frame [lst[0], lst[1], lst[2]] = True
#        self.blox.append (numpy.array ([lst[0], lst [1], lst [2]]))
        return self.fill3 (lst[0], lst [1], lst [2])


    def spitEmOut (self):
        try:
            x = [j.tolist () for j in self.blox]
        except AttributeError:
            print ("bad cubes in blox", self.blox)
        y = numpy.array (x)
        return y

    def has (self, voxel):
# arrays don't work like this        return voxel in self.blox
        found = False
        for y in self.blox:
            if numpy.all (y == voxel): found = True
        return found



# needs testing!!
    def __getitem__ (self, key):
#        return self.frame[key]
# unsure whether format is consistent here
#        print ("in getitem", key, key.__class__, numpy.mat (key), self.blox)

        return key in [j.tolist ()  for j in self.blox]

    def __str__ (self):
#        return self.frame.__str__ ()
        return self.spitEmOut ().__str__()


class BigCube (Cube):

    def __init__ (self):
        Cube.__init__(self, 4)


    def min (self):
# returns the lowest empty cell coordinate
        for row in range (4):
            for col in range (4):
                for layer in range (4):
                    if not self.has ([row, col, layer]):
                        return numpy.array ([row, col, layer])

    def insert (self, so, loc):
#totally untested - I think that there's an issue with updating self for this
        voidToFill = so.txlate (loc)
# should move these down below test
        c = BigCube ()
        c.blox = list (self.blox)
##        print ("v2f", voidToFill, so, loc, voidToFill.__class__, min ([h.min () for h in voidToFill.blox]),max ([h.max () for h in voidToFill.blox]))
        if (min ([h.min () for h in voidToFill.blox]) < 0) or (max ([h.max () for h in voidToFill.blox]) > 3):
##            print ("failed min")
            return (False, None)
        for cell in voidToFill.blox:
#            print ("filling cell", cell)
            if not (c.fill (cell)):
#                print (c)
                return (False, None)
#            print ("cell filled")
        return (True, c)



class Shape (Cube):

    rotz = numpy.array ([[0,1,0], [-1,0,0], [0,0,1]])
    roty = numpy.array ([[0,0,-1], [0,1,0], [1,0,0]])
    rotx = numpy.array ([[1,0,0], [0,0,1], [0,-1,0]])
    rot0 = numpy.array ([[1,0,0], [0,1,0], [0,0,1]])

    def __init__ (self, coordList):
        Cube.__init__ (self, 3)
        for i in coordList:
            assert (len (i) == 3), "wrong number of dimensions: %i, %s" % (len (i), i)
            self.fill (i)

    def txlate (self, vector):
# add vector to all of the filled in cubes of self
        x = Shape (self.spitEmOut ())
        s = Shape (x.spitEmOut () + vector)
        return s

    def rotator (self, rot, cube):
        s = Shape (self.spitEmOut ()).txlate (-self.blox [cube])
        c = numpy.dot(rot, s.spitEmOut ().transpose())
        return Shape (c.transpose ())


    def Rot0 (self, cube):
# algorithm: translate by coords of -cube, rotate around axis, translate by coords of +cube.
# maybe not include the xlate back?
        s = self.rotator (Shape.rot0, cube)
        return s

    def Rotx (self, cube):
# cube is which cube to iterate over, it's an index on the shape's filled in cubes
        return self.rotator (Shape.rotx, cube)

    def Roty (self, cube):
        return self.rotator (Shape.roty, cube)

    def Rotz (self, cube):
        return self.rotator (Shape.rotz, cube)
#        return Shape.rotz * numpy.mat (self.spitEmOut ())

class Shapes ():
    shapes = [Shape ([[1,0,0], [2,0,0], [1,1,0], [1,1,1], [0,2,0], [1,2,0]]),
         Shape ([[0,0,0], [0,1,0], [1,1,0], [1,2,0], [2,1,0], [2,1,1]]),
         Shape ([[2,0,0], [2,1,0], [1,1,0], [1,1,1], [0,1,0], [0,2,0]]),
         Shape ([[0,0,0], [1,0,0], [2,0,0], [0,1,0], [1,1,0], [2,0,1]]),
         Shape ([[0,0,0], [1,0,0], [0,1,0], [1,1,0], [1,2,0], [2,2,0]]),
         Shape ([[0,0,0], [1,0,0], [0,1,0], [1,1,0], [0,2,0], [0,2,1]]),
         Shape ([[0,0,0], [1,0,0], [2,0,0], [0,1,0], [2,1,0], [1,0,1]]),
         Shape ([[0,0,0], [1,0,0], [2,0,0], [0,1,0], [1,1,0], [2,1,0]]),
         Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,2,0], [1,0,1]]),
         Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]]),
         Shape ([[0,0,0], [1,0,0], [0,1,0], [0,1,1]])]
#something wrong with 8 (counting from zero)? looks disconnected on that last coord? should be 101


class testShape (unittest.TestCase):
    def setUp (self):
        x = [False for y in range (27)]
        y = numpy.array (x, dtype = bool)
        y.shape = (3,3,3)
        self.s = Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])

    def testInit (self):
        self.failUnless (self.s.filled () == 6)
        self.failUnless (self.s[1,1,1] == False)

# redundant?
    def testRot (self):
        s = Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])

        x = s.spitEmOut ()
        rotx = numpy.array ([[0,1,0], [-1,0,0], [0,0,1]])
        self.failUnless (numpy.all (numpy.dot (rotx, x.transpose ()) == numpy.array ([[1,0,1,2,0,2], [0,-1,-1,-1,-2,-2], [0,0,0,0,0,0]])))

    def testRotx (self):
#        self.failUnless (self.s.Rotx (1).__cmp__ (Shape ([[0,0,-1], [1,0,0], [1,0,-1], [1,0,-2], [2,0,0], [2,0,-2]])))
        self.failUnless (self.s.Rotx (1).__cmp__ (Shape ([[-1,0,-1], [0,0,0], [0,0,-1], [0,0,-2], [1,0,0], [1,0,-2]])))

    def testCmp (self):
        # not working yet as the various sorts don't seem do do what I thought they would
        m = Shape ([[2,1,0], [1,0,0], [1,1,0], [1,2,0], [0,0,0], [0,2,0]])
        n = Shape ([[2,1,0], [1,2,0], [1,1,0], [1,0,0], [0,2,0], [0,0,0]])
        o = Shape ([[1,0,0], [0,1,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])
        u = Shape ([[0,1,1], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])
        s1 = m.spitEmOut ().tolist ()
        s2 = n.spitEmOut ().tolist ()
#        print (s1, s2)
        s1.sort ()
        s2.sort ()
#        print (s1, s2, (s1 == s2))
        self.failUnless (self.s.__cmp__(o))
        self.failIf (self.s.__cmp__(u))
        self.failUnless (m.__cmp__(n))


    def testTxlate (self):
        self.failUnless (Shape.__cmp__ (self.s.txlate ([1,2,3]), Shape ([[1,3,3],[2,2,3],[2,3,3],[2,4,3],[3,2,3],[3,4,3]])))


class testBigCube (unittest.TestCase):

    def setUp (self):
        self.x = BigCube ()

    def test_init (self):
        pass
        #self.fail ("not yet implemented")

    def testMin (self):
        self.failUnless (numpy.all (self.x.min() == numpy.array ([0,0,0])))
# add in void, and check for correct min value

    def testInsert (self):
        (works, result) = self.x.insert (Shapes.shapes[0], [0,0,0])
        print ("test insert", works, result)
#        (works, result) = self.x.insert (so, loc)
        pass



# why are these in testBigCube?
    def testFill (self):
        self.assert_ (self.x.fill3 (1,1,1))
        self.assert_ (self.x.fill (numpy.array ([1,2,3])))
        self.failIf (self.x.fill (numpy.array ([1,1,1])))
        self.assert_ (not self.x.has (numpy.array ([1,1,0])))

    def testSpitEmOut (self):
        s = Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])
        self.failUnless (s.__cmp__(Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])))

class Usage (Exception):
    def __init__ (self, msg):
        self.msg = msg

psyco.full ()

def main (argv = None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt (argv [1:], "h", ["help"])
        except getopt.error as goe:
            raise Usage (goe.msg)
#        print (opts, args [0])

# more code here
    except Usage as err:
        print >> sys.stder, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

    bCSuite = unittest.makeSuite (testBigCube)
    suite = unittest.makeSuite (testShape)
    unittest.TextTestRunner (verbosity=2).run (bCSuite)
    unittest.TextTestRunner (verbosity=2).run (suite)

# loops that create the 144 voxels occupied by one shape, but eliminating duplicates
#    s = Shape ([[0,1,0], [1,0,0], [1,1,0], [1,2,0], [2,0,0], [2,2,0]])
#    s = Shape ([[1,0,0], [2,0,0], [1,1,0], [1,1,1], [0,2,0], [1,2,0]])
    s = Shapes.shapes [0]


    for ix in range (len (Shapes.shapes)):
        s = Shapes.shapes [ix]
        if False:
# maybe shapeSet is another object type with Shape as a component
#             shapeSet = set (s.Rot0 (1))
            shapeSet = [s.Rot0 (1)]
#             shapeSet = numpy.array ([s.Rot0 (1)])
            for l in range (s.filled ()):
                for i in range (4):
                    for j in range (4):
                        for k in range (4):
                            found = False
                            for x in shapeSet:
                                if x.__cmp__(s.Rotx (l)):
#                                    print ("found", x, s.Rotx (l))
                                    found = True
            
                            if not found: shapeSet.append (s.Rotx (l))
#                            if not found: numpy.append (shapeSet, s.Rotx (l))
                            s = s.Rotx (l)
                        s = s.Roty (l)
                    s = s.Rotz (l)
                print (len (shapeSet))
            Stuff.stuff ["%i" % ix] = shapeSet
    
#            pickle.dump (shapeSet, open ("wibble", "w"))
            pickle.dump (Stuff.stuff, open ("wibble", "w"))
    
    Stuff.stuff = pickle.load (open ("wibble.in", "r"))
    print (Stuff.stuff.keys ())

    print (datetime.datetime.now ())
    print (Stuff.stuff ["2"][0])

    count = 0
    todo = Stuff.stuff.keys ()
    for i in Stuff.stuff.keys ():
        shapeSet = Stuff.stuff [i]
        for s in range (len (shapeSet)):
# could do this with a guard space
            if (min ([h.min () for h in shapeSet [s].blox]) >=0) and (max ([h.max () for h in shapeSet [s].blox]) <=3):
                count += 1
#            print (count)
    print ("xxx", len (Stuff.stuff [todo [0]]))

    b = BigCube ()

    doIt (b, todo, {})


    c = BigCube ()
    d = Shape ([[0,0,2],[0,0,1],[0,0,0],[0,1,2],[0,1,1],[1,0,0]])
    print (c.insert (d, [0,0,0]), d, c)
    print (c.insert (Shape ([[0,0,0],[0,1,0],[0,1,-1],[0,2,-1],[0,1,-2],[1,1,-2]]), [0,0,3]))
#    for i in Shapes.shapes:
#         print (i)

def doIt (b, todo, completed):

#    if len (todo) <=2:  print (todo, b, b.filled ())
    if todo == []:
        print ("finished", b.filled ())
        return True
    else:
        lowest = b.min ()
        for x in todo:
# another loop needed here for each orientation, or a generator
            for y in Stuff.stuff [x]:
#                print ("y, lowest", y, lowest)
                (worked, a) = b.insert (y, lowest)
                if worked:
                    todo1 = list (todo)
                    todo1.remove (x)
                    if len (todo) <=2:
                         v = [blah.__str__() for blah in completed.values ()]
                         print (datetime.datetime.now ())
                         print (x, completed.keys (), v, todo, b.filled ())
#                        sys.stdout.flush ()
                    comp = completed.copy ()
                    comp [lowest.__str__()] = y
#                    print ("c", completed)
                    if doIt (a, todo1, comp):
                        print (x, y, lowest)
                        return True
        return False


#  b = BigCube, shapesLeft = {dict of shapeNames,shapeSets}
# 0.if shapesLeft is empty, we're done!
# 0a. find lowest empty voxel (possible check for impossible voids?)
# 1.for each shape;
# 2.for each shape orientation
# 3.drop SO, into BigCube at voxel, if overlap or out of bounds, give up
# 4.try again at 0. after removing the current shape from shapesLeft

if __name__ == "__main__":
    sys.exit (main ())

