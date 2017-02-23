set terminal postscript eps
set output "Fig2.eps"

set yrange [0:1.2]
set xlabel "network density"
set ylabel "goodness"
plot "Fig2.dat" u 1:2 w lp lt 1 lw 3 t "goodness", "Fig2.dat" u 1:3 w lp lt 2 lw 1 notitle, "Fig2.dat" u 1:4 w lp lt 2 lw 1 notitle