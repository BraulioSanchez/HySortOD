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
cmd = 'mkdir -p %s && rm -fr %s/%s_q4*' % (results_path, results_path, hysortod[0])
os.system(cmd)

# Run `q4_1` experiments
file = open('code/results/%s_q4_1.csv' % hysortod[0], 'w')
output = '%s\n' % ','.join(map(str, hysortod[3]))
file.write(output)
file.flush()

dictionary = model_configurations.configurations_categorical
for dataset in dictionary[hysortod[1]]:
    if dataset in datasets_list.datasets_numerical_categorical:
        command = (
            hysortod[2],
            datasets_list.datasets_numerical_categorical[dataset][0],
            datasets_list.datasets_numerical_categorical[dataset][1],
            dataset
        )
        dictionary[hysortod[1]][dataset](command)

        cmd = 'cat code/results/%s.csv >> code/results/%s_q4_1.csv && rm code/results/%s.csv' \
                % (hysortod[0], hysortod[0], hysortod[0])
        os.system(cmd)

file.close()

# Run `q4_2` experiments
file = open('code/results/%s_q4_2.csv' % hysortod[0], 'w')
output = '%s\n' % ','.join(map(str, hysortod[3]))
file.write(output)
file.flush()

configuration = model_configurations.configuration_hysortod_best_fixed
scenarios = datasets_list.datasets_synthetic_categorical
for variation in scenarios['scenario_1']:
    centers = scenarios['scenario_1'][variation]
    for center in centers:
        dataset, cols = centers[center]
        for i in range(10):
            command = (
                hysortod[2],
                dataset %  (i, 0),
                cols+i,
                'scenario_1/%s/%s/%d-rcat-%d-icat' % (variation, center, i, 0)
            )
            configuration(command)
            cmd = 'cat code/results/%s.csv >> code/results/%s_q4_2.csv && rm code/results/%s.csv' \
                    % (hysortod[0], hysortod[0], hysortod[0])
            os.system(cmd)            

        for i in range(1, 10):
            command = (
                hysortod[2],
                dataset %  (9, i),
                cols+9+i,
                'scenario_1/%s/%s/%d-rcat-%d-icat' % (variation, center, 9, i)
            )
            configuration(command)
            cmd = 'cat code/results/%s.csv >> code/results/%s_q4_2.csv && rm code/results/%s.csv' \
                    % (hysortod[0], hysortod[0], hysortod[0])
            os.system(cmd)

scenarios = datasets_list.datasets_synthetic_categorical
for variation in scenarios['scenario_2']:
    dataset, cols = scenarios['scenario_2'][variation]
    for i in range(10):
        command = (
            hysortod[2],
            dataset %  (i, 0),
            cols+i,
            'scenario_1/%s/%d-rcat-%d-icat' % (variation, i, 0)
        )
        configuration(command)
        cmd = 'cat code/results/%s.csv >> code/results/%s_q4_2.csv && rm code/results/%s.csv' \
                % (hysortod[0], hysortod[0], hysortod[0])
        os.system(cmd)            

    for i in range(1, 10):
        command = (
            hysortod[2],
            dataset %  (9, i),
            cols+9+i,
            'scenario_1/%s/%d-rcat-%d-icat' % (variation, 9, i)
        )
        configuration(command)
        cmd = 'cat code/results/%s.csv >> code/results/%s_q4_2.csv && rm code/results/%s.csv' \
                % (hysortod[0], hysortod[0], hysortod[0])
        os.system(cmd)

file.close()

# Process `q4_1` result
file = open('experiments/q4_categorical_data/result_1.txt', 'w')

hysortod = ["HySortOD", "hysortod", ['Runtime','AUROC','Dataset','b','minSplit']]

results_path = 'code/results/'
result_q1 = pd.read_csv('%s%s_q1.csv' % (results_path, hysortod[0]))
result_q4 = pd.read_csv('%s%s_q4_1.csv' % (results_path, hysortod[0]))
result = pd.concat([result_q1, result_q4], axis=0)
result = result.groupby(hysortod[2][2:]).mean().reset_index().query("b==5 & minSplit==100")

result_categorical_data = pd.DataFrame(columns=['Dataset','N','NC','NC-N'])
for dataset in datasets_list.datasets_numerical_categorical:
    numerical_dataset = dataset
    categorical_dataset = dataset.replace('-con','')
    
    query = 'Dataset=="%s"' % numerical_dataset
    n = result.query(query)['AUROC'].squeeze()
    query = 'Dataset=="%s"' % categorical_dataset
    nc = result.query(query)['AUROC'].squeeze()

    row = [categorical_dataset, n, nc, nc-n]
    result_categorical_data.loc[len(result_categorical_data)] = row

file.write(result_categorical_data.to_string(index=False))
file.flush()

# Process `q4_2` result
hysortod = ["HySortOD", "hysortod", ['Runtime','AUROC','Dataset','b','minSplit']]

results_path = 'code/results/'
result = pd.read_csv('%s%s_q4_2.csv' % (results_path, hysortod[0]))
result = result.groupby(hysortod[2][2:]).mean().reset_index()

result.to_csv('experiments/q4_categorical_data/result_2.csv', index=False)