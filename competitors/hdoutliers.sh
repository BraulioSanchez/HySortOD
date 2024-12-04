#!/bin/bash

export RCommand="Rscript competitors/HDoutliers/script.R"
name="HDoutliers"

$RCommand \
$1 \
$3 \
$4 > /dev/null

if [ ! -d competitors/HDoutliers/results ]; then
    mkdir -p competitors/HDoutliers/results
fi

export javaCommand="java -jar competitors/HDoutliers/analyze/analyze-0.0.1-SNAPSHOT.jar"

if [ ! -d competitors/results ]; then
    mkdir -p competitors/results
fi

$javaCommand \
--input $1 \
--labelColumn $2 > $name.log
auroc=$(cat $name.log | grep -oP 'auroc \K\d+\.\d+')
echo "$3,$auroc,-1,$4" >> competitors/results/$name.csv
rm $name.log