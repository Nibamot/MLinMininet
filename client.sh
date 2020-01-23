#!/bin/bash

server=(10.0.0.1 10.0.0.2)
timeint=(40 50 70 80 90 100 120 150 200)
# 20 30 40 50 60 70 80 90 100)
bw=(10M 25M 50M 75M 100M)

for((trial=1;trial<=1;trial++))
do
  for i in "${timeint[@]}"
  do
    for j in "${bw[@]}"
    do
      iperf3 -c 10.0.0.1 -p 5001 -t $i -u -b $j -l 1460
      sleep 2
    done
  done
done
