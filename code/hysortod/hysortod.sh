#!/bin/bash

export javaCommand="java -Xmx10G -jar code/hysortod/target/HySortOD-1.0.jar"
name="HySortOD"

if [ ! -d code/results ]; then
    mkdir -p code/results
fi

for _ in {1..10}
do
    $javaCommand \
    --input $1 \
    --labelColumn $2 \
    --b $4 \
    --minSplit $5 > $name.log
    auroc=$(cat $name.log | grep -oP 'auroc \K\d+\.\d+')
    runtime=$(cat $name.log | grep -oP 'runtime \K\d+\.\d+')
    echo "$3,$auroc,$runtime,$4,$5" >> code/results/$name.csv
    rm $name.log
done