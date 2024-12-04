#!/bin/bash

export javaCommand="java -Xmx10G -jar competitors/elki-0.8.0.jar KDDCLIApplication"
algorithm="outlier.lof.ALOCI"
name="aLOCI"

if [ ! -d competitors/results ]; then
    mkdir -p competitors/results
fi

for _ in {1..10}
do
    $javaCommand \
    -algorithm $algorithm \
    -time \
    -dbc.in $1 \
    -parser.labelIndices $2 \
    -loci.nmin $4 \
    -loci.g $5 \
    -loci.seed $((1 + RANDOM % 2147483647)) > $name.log
    auroc=$(cat $name.log | grep -oP 'measures AUROC \K\d+\.\d+')
    runtime=$(cat $name.log | grep -oP 'runtime: \K\d+')
    echo "$3,$auroc,$runtime,$4,$5" >> competitors/results/$name.csv
done
rm $name.log