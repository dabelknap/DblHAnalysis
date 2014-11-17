#!/bin/bash

cd $1

for mass in $(ls);
do
    cd $mass
    combineCards.py *.txt > merged.out
    combine -m $mass -M Asymptotic merged.out
    cd ..
done

cd ..
