set xrange [0:3]
set yrange [0:3]
set zrange [0:3]

set pointsize 3
set style line 2 lt 2 lw 6
splot "p0"  with points 2 , "p1" with points 3, "p2" with points 4, "p3" with points 5, "p4" with points 6, "p5" with points 1, "p6" with points 7, "p7" with points 8, "p10" with points 9
