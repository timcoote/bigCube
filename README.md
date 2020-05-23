prog to solve wooden cube by brute force recursive space filler.
Answers are in the various p files and answers.

I cannot remember how the various files fit together, but there are clearly
separate processing stages involved before finally spitting out a gnuplot
readable set of data. the latter may even have been hand crafted.
to plot the answer just run gnuplot and load the plot file (load "plot")
gnuplot is broken on F14.

more fun: psyco has gone from F14. F15 has pypy, but that doesn't support
numpy! Bottome line, the answers are there, but it wouldn't make sense to 
rerun the program, I don't think.

Added a git repo and fixed some changes to the point types. 3d plot is not 
easy to use now as the point styles are in odd colours and the legend
overlays the image

# Description of Algorithm

Object types:
- Cube (size): a representation of a cube of length `size` voxels on each side
- BigCube ():  a representation of the 4x4 completed wooden cube. The key method
on this type (which needs a test or two), is `insert (shape, location)`, which takes
a shape (wooden blocks in a particular orientation) and, if they fit into the object
returns the new object with them added. If they don't (overlap occupied voxel, or
include voxels outside of the bigCube). It returns False.
- Stuff:       a class to hold the various occupancy patterns of the individual
               shapes that go into the wooden cube.

- Shape:       a generic class of 3d voxels. This class defines the operaitons on
a shape (rotatioons and translations) that can be used to find all possible sets of 
voxels that this shape could occupy
- Shapes ():   the voxels in each of the primitive wooden shapes


`main` is split into two parts, with a feature toggle on the first. The first
bit caches all positions that each shape can be dropped into bigCube. These 
are held in the dictionoary `Stuff.stuff`. The key is the index of the shape in `Shapes`
The results are cached in `wibble`

For the second part, `wibble.in` is used as input (originally called `wibble`!, but renamed
to avoid accidentally destroying this cache.
This is a brute force approach to inserting all orientations of all shapes into bigCube, at
the `lowest` location, until, eithr the bigCube is full, or there are shapes that will not fit in.

