#!/bin/bash

export javaCommand="java -Xmx10G -jar competitors/elki-0.8.0.jar KDDCLIApplication"
algorithm="outlier.distance.KNNOutlier"
name="kNN-Out"

if [ ! -d competitors/results ]; then
    mkdir -p competitors/results
fi

$javaCommand \
-algorithm $algorithm \
-time \
-dbc.in $1 \
-parser.labelIndices $2 \
-knno.k $4 > $name.log
auroc=$(cat $name.log | grep -oP 'measures AUROC \K\d+\.\d+')
runtime=$(cat $name.log | grep -oP 'runtime: \K\d+')
echo "$3,$auroc,$runtime,$4" >> competitors/results/$name.csv
rm $name.log