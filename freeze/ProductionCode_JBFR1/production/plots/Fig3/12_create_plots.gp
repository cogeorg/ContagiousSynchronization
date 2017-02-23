set terminal postscript eps
set key font ",30"
set xtics font ",20"
set ytics font ",20"
set xlabel font ",30"
set key bottom



set output "Fig3--rand-density.eps"
set yrange [0:1.2]
set ylabel font ",30"
set ylabel "goodness" offset -1,0,0
plot "Fig3--rand-density.dat" u 1:4 w lp lt 1 lw 3 t "Random", "Fig3--rand-density.dat" u 1:5 w lp lt 2 lw 1 notitle, "Fig3--rand-density.dat" u 1:6 w lp lt 2 lw 1 notitle

set output "Fig3--rand-path_length.eps"
set yrange [0:1.2]
unset ylabel
plot "Fig3--rand-path_length.dat" u 2:4 w lp lt 1 lw 3 t "Random", "Fig3--rand-path_length.dat" u 2:5 w lp lt 2 lw 1 notitle, "Fig3--rand-path_length.dat" u 2:6 w lp lt 2 lw 1 notitle

set output "Fig3--rand-clustering.eps"
set yrange [0:1.2]
plot "Fig3--rand-clustering.dat" u 3:4 w lp lt 1 lw 3 t "Random", "Fig3--rand-clustering.dat" u 3:5 w lp lt 2 lw 1 notitle, "Fig3--rand-clustering.dat" u 3:6 w lp lt 2 lw 1 notitle



set output "Fig3--ba-density.eps"
set yrange [0:1.2]
set ylabel font ",30"
set ylabel "goodness" offset -1,0,0
plot "Fig3--ba-density.dat" u 1:4 w lp lt 1 lw 3 t "Barabasi-Albert", "Fig3--ba-density.dat" u 1:5 w lp lt 2 lw 1 notitle, "Fig3--ba-density.dat" u 1:6 w lp lt 2 lw 1 notitle

set output "Fig3--ba-path_length.eps"
set yrange [0:1.2]
unset ylabel
plot "Fig3--ba-path_length.dat" u 2:4 w lp lt 1 lw 3 t "Barabasi-Albert", "Fig3--ba-path_length.dat" u 2:5 w lp lt 2 lw 1 notitle, "Fig3--ba-path_length.dat" u 2:6 w lp lt 2 lw 1 notitle

set output "Fig3--ba-clustering.eps"
set yrange [0:1.2]
plot "Fig3--ba-clustering.dat" u 3:4 w lp lt 1 lw 3 t "Barabasi-Albert", "Fig3--ba-clustering.dat" u 3:5 w lp lt 2 lw 1 notitle, "Fig3--ba-clustering.dat" u 3:6 w lp lt 2 lw 1 notitle



set output "Fig3--ws-density.eps"
set yrange [0:1.2]
set ylabel font ",30"
set xlabel "network density" offset 0,-1,0
set ylabel "goodness" offset -1,0,0
plot "Fig3--ws-density.dat" u 1:4 w lp lt 1 lw 3 t "Watts-Strogatz", "Fig3--ws-density.dat" u 1:5 w lp lt 2 lw 1 notitle, "Fig3--ws-density.dat" u 1:6 w lp lt 2 lw 1 notitle

set output "Fig3--ws-path_length.eps"
set yrange [0:1.2]
set xlabel "shortest average path length"  offset 0,-1,0
unset ylabel
plot "Fig3--ws-path_length.dat" u 2:4 w lp lt 1 lw 3 t "Watts-Strogatz", "Fig3--ws-path_length.dat" u 2:5 w lp lt 2 lw 1 notitle, "Fig3--ws-path_length.dat" u 2:6 w lp lt 2 lw 1 notitle

set output "Fig3--ws-clustering.eps"
set yrange [0:1.2]
set xlabel "clustering" offset 0,-1,0
plot "Fig3--ws-clustering.dat" u 3:4 w lp lt 1 lw 3 t "Watts-Strogatz", "Fig3--ws-clustering.dat" u 3:5 w lp lt 2 lw 1 notitle, "Fig3--ws-clustering.dat" u 3:6 w lp lt 2 lw 1 notitle
