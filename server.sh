#!/bin/bash
interval=(2 2.5 3.0 4.0 5.0)
#(2 2.5 3.0 4.0 5.0)
#0.5 1 1.5 2 2.5
for((trial=1;trial<=9;trial++))
do
  for i in "${interval[@]}"
  do
    cat data1.txt >> trainingdata1.txt
    iperf3 -s -1 -i $i -p 5001 > h1sh3c.txt
    python datatrim1.py
  done
done
