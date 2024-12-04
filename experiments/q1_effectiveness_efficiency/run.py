import os
import sys

script_dir = os.path.dirname(__file__)
modules_dir = os.path.join(script_dir, '..')
sys.path.append(modules_dir)

import datasets_list
import model_configurations

import pandas as pd
import numpy as np

# Runs for HySortOD
hysortod = ["HySortOD", "hysortod", "code/hysortod/hysortod.sh", ['Dataset','AUROC','Runtime','b','minSplit']]

# Clean `results` path
results_path = 'code/results/'
cmd = 'mkdir -p %s && rm -fr %s/%s_q1.csv' % (results_path, results_path, hysortod[0])
os.system(cmd)

file = open('code/results/%s_q1.csv' % hysortod[0], 'w')
output = '%s\n' % ','.join(map(str, hysortod[3]))
file.write(output)
file.flush()

# Run `q1` experiments
dictionary = model_configurations.configurations
for dataset in dictionary[hysortod[1]]:
    if dataset in datasets_list.datasets_all:
        command = (
            hysortod[2],
            datasets_list.datasets_all[dataset][0],
            datasets_list.datasets_all[dataset][1],
            dataset
        )
        dictionary[hysortod[1]][dataset](command)

        cmd = 'cat code/results/%s.csv >> code/results/%s_q1.csv && rm code/results/%s.csv' \
                % (hysortod[0], hysortod[0], hysortod[0])
        os.system(cmd)

file.close()

# Runs for Competitors
competitors = [
    ["iForest", "iforest", "competitors/iforest.sh", ['Dataset','AUROC','Runtime','h','ψ']],
    ["HDoutliers", "htoutliers", "competitors/hdoutliers.sh", ['Dataset','AUROC','Runtime','alpha']],
]

for competitor in competitors:
    # Clean `results` path
    results_path = 'competitors/results/'
    cmd = 'mkdir -p %s && rm -fr %s/%s_q1.csv' % (results_path, results_path, competitor[0])
    os.system(cmd)

    file = open('competitors/results/%s_q1.csv' % competitor[0], 'w')
    output = '%s\n' % ','.join(map(str, competitor[3]))
    file.write(output)
    file.flush()

    dictionary = model_configurations.configurations
    for dataset in dictionary[competitor[1]]:
        command = (
            competitor[2],
            datasets_list.datasets_all[dataset][0],
            datasets_list.datasets_all[dataset][1],
            dataset
        )
        dictionary[competitor[1]][dataset](command)
        
        cmd = 'cat competitors/results/%s.csv >> competitors/results/%s_q1.csv && rm competitors/results/%s.csv' \
            % (competitor[0], competitor[0], competitor[0])
        # print(cmd)
        os.system(cmd)

    file.close()

# Runs for Other competitors
other_competitors = [
    ["kNN-Out", "knnoutlier", "competitors/knnoutlier.sh", ['Dataset','AUROC','Runtime','k']],
    ["DB-Out", "dbout", "competitors/dbout.sh", ['Dataset','AUROC','Runtime','d']],
    ["LOF", "lof", "competitors/lof.sh", ['Dataset','AUROC','Runtime','k']],
    ["ODIN", "odin", "competitors/odin.sh", ['Dataset','AUROC','Runtime','k']],
    ["HilOut", "hilout", "competitors/hilout.sh", ['Dataset','AUROC','Runtime','k','h']],
    ["aLOCI", "aloci", "competitors/aloci.sh", ['Dataset','AUROC','Runtime','k','h']],
    ["ABOD", "abod", "competitors/abod.sh", ['Dataset','AUROC','Runtime','_']],
]

for competitor in other_competitors:
    # Clean `results` path
    results_path = 'competitors/results/'
    cmd = 'mkdir -p %s && rm -fr %s/%s_q1.csv' % (results_path, results_path, competitor[0])
    os.system(cmd)

    file = open('competitors/results/%s_q1.csv' % competitor[0], 'w')
    output = '%s\n' % ','.join(map(str, competitor[3]))
    file.write(output)
    file.flush()

    dictionary = model_configurations.configurations
    for dataset in dictionary[competitor[1]]:
        command = (
            competitor[2],
            datasets_list.datasets_numerical_without_header[dataset][0],
            datasets_list.datasets_numerical_without_header[dataset][1],
            dataset
        )
        dictionary[competitor[1]][dataset](command)

        cmd = 'cat competitors/results/%s.csv >> competitors/results/%s_q1.csv && rm competitors/results/%s.csv' \
            % (competitor[0], competitor[0], competitor[0])
        os.system(cmd)        

    file.close()

# Process `q1` result
file = open('experiments/q1_effectiveness_efficiency/result.txt', 'w')

hysortod = ["HySortOD", "hysortod", "code/hysortod/hysortod.sh", ['AUROC','Runtime','Dataset','b','minSplit']]
output = '[%s]\n' % hysortod[0]
file.write(output)
file.flush()

results_path = 'code/results/'
result = pd.read_csv('%s%s_q1.csv' % (results_path, hysortod[0]))
result = result.groupby(hysortod[3][2:]).mean().reset_index()

_result = result.groupby(hysortod[3][3:]).mean().reset_index()
best_params = pd.DataFrame(_result.iloc[_result['AUROC'].argmax(),:][hysortod[3][3:]]).transpose()
result_best_fixed = pd.merge(result, best_params, on=hysortod[3][3:], how='inner')

output = 'Best-fixed:\n%s\n' % result_best_fixed.to_string(index=False)
file.write(output)
file.flush()

result_best = pd.DataFrame()
for dataset in list(datasets_list.datasets_all.keys()):
    _result = result.query('Dataset == "%s"' % dataset)
    _result_best = _result[_result['AUROC'] == _result['AUROC'].max()]
    if(_result_best.size > 0):
        result_best = result_best.append(_result_best)

output = 'Best:\n%s\n' % result_best.to_string(index=False)
file.write(output)
file.flush()

competitors = [
    ["iForest", "iforest", "competitors/iforest.sh", ['AUROC','Runtime','Dataset','h','ψ']],
    ["HDoutliers", "htoutliers", "competitors/hdoutliers.sh", ['AUROC','Dataset','Runtime','alpha']],
    ["kNN-Out", "knnoutlier", "competitors/knnoutlier.sh", ['AUROC','Runtime','Dataset','k']],
    ["DB-Out", "dbout", "competitors/dbout.sh", ['AUROC','Runtime','Dataset','d']],
    ["LOF", "lof", "competitors/lof.sh", ['AUROC','Runtime','Dataset','k']],
    ["ODIN", "odin", "competitors/odin.sh", ['AUROC','Runtime','Dataset','k']],
    ["HilOut", "hilout", "competitors/hilout.sh", ['AUROC','Runtime','Dataset','k','h']],
    ["aLOCI", "aloci", "competitors/aloci.sh", ['AUROC','Runtime','Dataset','k','h']],
    ["ABOD", "abod", "competitors/abod.sh", ['AUROC','Runtime','Dataset','_']],
]

for competitor in competitors:
    output = '[%s]\n' % competitor[0]
    file.write(output)
    file.flush()

    results_path = 'competitors/results/'
    result = pd.read_csv('%s%s_q1.csv' % (results_path, competitor[0]))
    result = result.groupby(competitor[3][2:]).mean().reset_index()
    
    _result = result.groupby(competitor[3][3:]).mean().reset_index()
    best_params = pd.DataFrame(_result.iloc[_result['AUROC'].argmax(),:][competitor[3][3:]]).transpose()
    result_best_fixed = pd.merge(result, best_params, on=competitor[3][3:], how='inner')
    
    output = 'Best-fixed:\n%s\n' % result_best_fixed.to_string(index=False)
    file.write(output)
    file.flush()

    result_best = pd.DataFrame()
    for dataset in list(datasets_list.datasets_all.keys()):
        _result = result.query('Dataset == "%s"' % dataset)
        _result_best = _result[_result['AUROC'] == _result['AUROC'].max()]
        if(_result_best.size > 0):
            result_best = result_best.append(_result_best)

    output = 'Best:\n%s\n' % result_best.to_string(index=False)
    file.write(output)
    file.flush()