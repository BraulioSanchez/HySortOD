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

# Build `results` path
results_path = 'code/results/'
cmd = 'mkdir -p %s && rm -fr %s/%s_q2.csv' % (results_path, results_path, hysortod[0])
os.system(cmd)

file = open('code/results/%s_q2.csv' % hysortod[0], 'w')
output = '%s\n' % ','.join(map(str, hysortod[3]))
file.write(output)
file.flush()

# Run `q2` experiments
dictionary = model_configurations.configurations_scalability
for dataset in dictionary[hysortod[1]]:
    for i in [1, 2, 10, 25, 50, 100]:
        command = (
            hysortod[2],
            datasets_list.datasets_scalability[dataset][0] % i,
            datasets_list.datasets_scalability[dataset][1],
            dataset + '_%sperc' % i
        )
        dictionary[hysortod[1]][dataset](command)    

        cmd = 'cat code/results/%s.csv >> code/results/%s_q2.csv && rm code/results/%s.csv' \
                % (hysortod[0], hysortod[0], hysortod[0])
        os.system(cmd)

file.close()

# Runs for Competitors
competitors = [
    ["iForest", "iforest","competitors/iforest.sh", ['Dataset','AUROC','Runtime','h','ψ']],
    ["kNN-Out", "knnoutlier", "competitors/knnoutlier.sh", ['Dataset','AUROC','Runtime','k']],
    ["DB-Out", "dbout", "competitors/dbout.sh", ['Dataset','AUROC','Runtime','d']],
    ["LOF", "lof", "competitors/lof.sh", ['Dataset','AUROC','Runtime','k']],
    ["ODIN", "odin", "competitors/odin.sh", ['Dataset','AUROC','Runtime','k']],
    ["HilOut", "hilout", "competitors/hilout.sh", ['Dataset', 'AUROC','Runtime','k','h']],
    ["aLOCI", "aloci", "competitors/aloci.sh", ['Dataset','AUROC','Runtime','k','h']],
    ["ABOD", "abod", "competitors/abod.sh", ['Dataset','AUROC','Runtime','_']],    
]

for competitor in competitors:
    # Clean `results` path
    results_path = 'competitors/results/'
    cmd = 'mkdir -p %s && rm -fr %s/%s_q2.csv' % (results_path, results_path, competitor[0])
    os.system(cmd)

    file = open('competitors/results/%s_q2.csv' % competitor[0], 'w')
    output = '%s\n' % ','.join(map(str, competitor[2]))
    file.write(output)
    file.flush()

    dictionary = model_configurations.configurations_scalability
    for scenario in dictionary[competitor[1]]:
        for i in [1, 2, 10, 25, 50, 100]:
            command = (
                competitor[2],
                datasets_list.datasets_scalability[scenario][0] % i,
                datasets_list.datasets_scalability[scenario][1],
                scenario + '_%sperc' % i
            )
            dictionary[competitor[1]][scenario](command)        
        
            cmd = 'cat competitors/results/%s.csv >> competitors/results/%s_q2.csv && rm competitors/results/%s.csv' \
                % (competitor[0], competitor[0], competitor[0])
            os.system(cmd)

    file.close()

# Process `q2` result
hysortod = ["HySortOD", "hysortod", ['AUROC','Runtime','Dataset','b','minSplit']]

results_path = 'code/results/'
result = pd.read_csv('%s%s_q2.csv' % (results_path, hysortod[0]))
result = result.groupby(hysortod[2][2:]).mean().reset_index()[hysortod[2][1:3]]

result_scalability = pd.DataFrame()
ns = []
methods = []

for dataset in model_configurations.configurations_scalability[hysortod[1]]:
    n = datasets_list.datasets_scalability[dataset][2]
    for i in [1, 2, 10, 25, 50, 100]:
        query = 'Dataset=="%s_%sperc"' % (dataset,i)
        _result = result.query(query)
        result_scalability = result_scalability.append(_result)
        methods.append(hysortod[0])
        ns.append(int(n*(i/100)))

competitors = [
    ["iForest", "iforest",['AUROC','Runtime','Dataset','h','ψ']],
    ["kNN-Out", "knnoutlier", ['AUROC','Runtime','Dataset','k']],
    ["DB-Out", "dbout", ['AUROC','Runtime','Dataset','d']],
    ["LOF", "lof", ['AUROC','Runtime','Dataset','k']],
    ["ODIN", "odin", ['AUROC','Runtime','Dataset','k']],
    ["HilOut", "hilout", ['AUROC','Runtime','Dataset','k','h']],
    ["aLOCI", "aloci", ['AUROC','Runtime','Dataset','k','h']],
    ["ABOD", "abod", ['AUROC','Runtime','Dataset','_']],    
]

for competitor in competitors:
    results_path = 'competitors/results/'
    result = pd.read_csv('%s%s_q2.csv' % (results_path, competitor[0]))
    result = result.groupby(competitor[2][2:]).mean().reset_index()[competitor[2][1:3]]

    for dataset in model_configurations.configurations_scalability[competitor[1]]:
        n = datasets_list.datasets_scalability[dataset][2]
        for i in [1, 2, 10, 25, 50, 100]:
            query = 'Dataset=="%s_%sperc"' % (dataset,i)
            _result = result.query(query)
            if _result.shape[0] > 0:
                result_scalability = result_scalability.append(_result)
                methods.append(competitor[0])
                ns.append(int(n*(i/100)))

result_scalability.insert(0, 'Method', methods)
result_scalability.insert(1, 'n', ns)
result_scalability[['Method','Dataset','n','Runtime']].to_csv('experiments/q2_scalability/result.csv', index=False)