#!/usr/bin/gnuplot
reset

set terminal png size 800,600
set output "data.png"
set grid

#set terminal dumb

set xdata time
set timefmt "%m/%d/%y"
set xrange ["05/26/16" : "06/02/16"]
set format x "%m/%d"
#set timefmt "%m/%d/%y %H:%M"

set style data points
set key reverse Left outside
set ylabel "(mg/dL)"
set xlabel "Date"

plot "data" using 1:2 with points
