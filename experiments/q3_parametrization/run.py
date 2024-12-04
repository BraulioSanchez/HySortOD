import os
import sys

script_dir = os.path.dirname(__file__)
modules_dir = os.path.join(script_dir, '..')
sys.path.append(modules_dir)

import pandas as pd
import numpy as np

hysortod = ["HySortOD", "hysortod", ['Runtime','AUROC','Dataset','b','minSplit']]

results_path = 'code/results/'
result = pd.read_csv('%s%s_q1.csv' % (results_path, hysortod[0]))
result = result.groupby(hysortod[2][2:]).mean().reset_index()

# Process `q3` result
result_parametrization = result.query('b>=2 & b<=40')
result_parametrization.to_csv('experiments/q3_parametrization/result.csv', index=False)