#!/bin/bash
for i in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 ; do cat doPlots--prepare.R | R --no-save --args Fig3--0.4-0.6-$i network_density $i ; done

touch Fig3--0.4-0.6-res-network_density.dat
rm Fig3--0.4-0.6-res-network_density.dat
for i in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0  ; do cat Fig3--0.4-0.6-$i-res-average_density.dat >> Fig3--0.4-0.6-res-network_density.dat ; done 