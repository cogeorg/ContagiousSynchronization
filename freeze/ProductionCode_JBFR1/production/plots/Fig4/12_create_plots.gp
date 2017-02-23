set terminal postscript eps
set output "Fig4.eps"

set yrange [0:1.2]
set xlabel "probability of agents being informed"
set ylabel "goodness"
plot "Fig4.dat" u 10:4 w lp lt 1 lw 3 t "network density=0.1", "Fig4.dat" u 10:5 w lp lt 2 lw 1 notitle, "Fig4.dat" u 10:6 w lp lt 2 lw 1 notitle, "Fig4-0.5.dat" u 10:4 w lp lt 3 lw 3 t "network density=0.5", "Fig4-0.5.dat" u 10:5 w lp lt 4 lw 1 notitle, "Fig4-0.5.dat" u 10:6 w lp lt 4 lw 1 notitle