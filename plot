set xrange [0:3]
set yrange [0:3]
set zrange [0:3]

set pointsize 3
set style line 2 lt 2 lw 6
splot "p0"  with points, "p1" with points, "p2" with points, "p3" with points, "p4" with points, "p5" with points, "p6" with points, "p7" with points, "p10" with points;
