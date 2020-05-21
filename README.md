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
