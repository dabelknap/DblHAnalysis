#!/bin/bash

run_limits()
{
    cd $1

    for mass in $(ls);
    do
        cd $mass
        combineCards.py *.txt > merged.out
        combine -m $mass -M Asymptotic merged.out
        cd ..
    done

    cd ..
}

if [ $1 == "all" ]; then
    for BP in BP1 BP2 BP3 BP4 ee100 mm100 em100 mt100 et100; do
        run_limits $BP
    done
elif [ $1 == "clear" ]; then
    rm ./*/*/roo*
    rm ./*/*/*.root
    rm ./*/*/*.out
else
    run_limits $1
fi
