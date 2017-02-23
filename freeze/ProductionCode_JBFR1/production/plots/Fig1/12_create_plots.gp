set terminal postscript eps
set output "Fig1.eps"

set yrange [0:1.2]
set xlabel "network density"
set ylabel "average action"
plot "0.25-0.75-res-actions.dat" u 1:2 w lp lw 3 t "mu_0=0.25 , mu_1=0.75", "0.4-0.6-res-actions.dat" u 1:2 w lp lw 3 t "mu_0=0.40 , mu_1=0.60", "0.49-0.51-res-actions.dat" u 1:2 w lp lw 3 t "mu_0=0.49 , mu_1=0.51"