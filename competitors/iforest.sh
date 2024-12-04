#!/bin/bash

export javaCommand="java -Xmx10G -jar competitors/iforest-1.0.jar"
name="iForest"

if [ ! -d competitors/results ]; then
    mkdir -p competitors/results
fi

for _ in {1..10}
do
    $javaCommand \
    --input $1 \
    --labelColumn $2 \
    --seed $((1 + RANDOM % 2147483647)) \
    --h $4 \
    --ψ $5 > $name.log
    auroc=$(cat $name.log | grep -oP 'auroc \K\d+\.\d+')
    runtime=$(cat $name.log | grep -oP 'runtime \K\d+')
    echo "$3,$auroc,$runtime,$4,$5" >> competitors/results/$name.csv
    rm $name.log
done