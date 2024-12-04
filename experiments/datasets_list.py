datasets_all = {
    # ----------- numerical
    'parkinson': ['datasets/numerical/parkinson.csv', 22],
    'glass': ['datasets/numerical/glass.csv', 9],
    'ionosphere': ['datasets/numerical/ionosphere.csv', 33],
    'breastw': ['datasets/numerical/breastw.csv', 9],
    'pima': ['datasets/numerical/pima.csv', 8],
    'thyroid': ['datasets/numerical/thyroid.csv', 6],
    'satimage2': ['datasets/numerical/satimage2.csv', 36],
    'mammography': ['datasets/numerical/mammography.csv', 6],
    'shuttle': ['datasets/numerical/shuttle.csv', 9],
    'http': ['datasets/numerical/http.csv', 3],
    # ----------- categorical
    'hepatitis': ['datasets/categorical/hepatitis.csv', 20],
    'tae': ['datasets/categorical/tae.csv', 5],
    'lymphography': ['datasets/categorical/lymphography.csv', 18],
    'heart': ['datasets/categorical/heart.csv', 13],
    'ecoli': ['datasets/categorical/ecoli.csv', 7],
    'crx': ['datasets/categorical/crx.csv', 15],
    'australian': ['datasets/categorical/australian.csv', 14],
    'anneal': ['datasets/categorical/anneal.csv', 10],
    'german': ['datasets/categorical/german.csv', 20],
    'cmc': ['datasets/categorical/cmc.csv', 9],
    'car': ['datasets/categorical/car.csv', 6],
    'nursery': ['datasets/categorical/nursery.csv', 8],
    'adult': ['datasets/categorical/adult.csv', 14],
    'poker_hand': ['datasets/categorical/poker_hand.csv', 10]
}

datasets_numerical_without_header = {
    'parkinson': ['datasets/numerical/without_header/parkinson.csv', 22],
    'glass': ['datasets/numerical/without_header/glass.csv', 9],
    'ionosphere': ['datasets/numerical/without_header/ionosphere.csv', 33],
    'breastw': ['datasets/numerical/without_header/breastw.csv', 9],
    'pima': ['datasets/numerical/without_header/pima.csv', 8],
    'thyroid': ['datasets/numerical/without_header/thyroid.csv', 6],
    'satimage2': ['datasets/numerical/without_header/satimage2.csv', 36],
    'mammography': ['datasets/numerical/without_header/mammography.csv', 6],
    'shuttle': ['datasets/numerical/without_header/shuttle.csv', 9],
    'http': ['datasets/numerical/without_header/http.csv', 3]
}

datasets_scalability = {
    'http': ['datasets/scalability/http/http_%sperc.csv', 3, 567498],
    'http_without_header': ['datasets/scalability/http/without_header/http_%sperc.csv', 3, 567498],
    'poker_hand': ['datasets/scalability/poker_hand/poker_hand_%sperc.csv', 10, 1025010],
}

datasets_numerical_categorical = {
    'hepatitis-con': ['datasets/categorical/hepatitis-con.csv', 6],
    'tae-con': ['datasets/categorical/tae-con.csv', 2],
    'lymphography-con': ['datasets/categorical/lymphography-con.csv', 3],
    'heart-con': ['datasets/categorical/heart-con.csv', 7],
    'ecoli-con': ['datasets/categorical/ecoli-con.csv', 5],
    'crx-con': ['datasets/categorical/crx-con.csv', 6],
    'australian-con': ['datasets/categorical/australian-con.csv', 6],
    'anneal-con': ['datasets/categorical/anneal-con.csv', 6],
    'german-con': ['datasets/categorical/german-con.csv', 7],
    'cmc-con': ['datasets/categorical/cmc-con.csv', 5],
    'car-con': ['', 0],
    'nursery-con': ['', 0],
    'adult-con': ['datasets/categorical/adult-con.csv', 6],
    'poker_hand-con': ['', 0],
}

datasets_synthetic_categorical = {
    'scenario_1': {
        'varying_avg': {
            '250_750': ['datasets/synthetic/scenario_1/varying_avg/250_750/scenario-1-%d-rcat-%d-icat.csv', 6],
            '300_700': ['datasets/synthetic/scenario_1/varying_avg/300_700/scenario-1-%d-rcat-%d-icat.csv', 6],
            '350_650': ['datasets/synthetic/scenario_1/varying_avg/350_650/scenario-1-%d-rcat-%d-icat.csv', 6],
            '400_600': ['datasets/synthetic/scenario_1/varying_avg/400_600/scenario-1-%d-rcat-%d-icat.csv', 6],
            '450_550': ['datasets/synthetic/scenario_1/varying_avg/450_550/scenario-1-%d-rcat-%d-icat.csv', 6],
            '500_500': ['datasets/synthetic/scenario_1/varying_avg/500_500/scenario-1-%d-rcat-%d-icat.csv', 6],
        },
        'varying_att': {
            '0': ['datasets/synthetic/scenario_1/varying_att/0/scenario-1-%d-rcat-%d-icat.csv', 6],
            '1': ['datasets/synthetic/scenario_1/varying_att/1/scenario-1-%d-rcat-%d-icat.csv', 6],
            '2': ['datasets/synthetic/scenario_1/varying_att/2/scenario-1-%d-rcat-%d-icat.csv', 6],
            '3': ['datasets/synthetic/scenario_1/varying_att/3/scenario-1-%d-rcat-%d-icat.csv', 6],
            '4': ['datasets/synthetic/scenario_1/varying_att/4/scenario-1-%d-rcat-%d-icat.csv', 6],
            '5': ['datasets/synthetic/scenario_1/varying_att/5/scenario-1-%d-rcat-%d-icat.csv', 6],
        }
    },
    'scenario_2': {
        '005': ['datasets/synthetic/scenario_2/005/scenario-2-%d-rcat-%d-icat.csv', 6],
        '010': ['datasets/synthetic/scenario_2/010/scenario-2-%d-rcat-%d-icat.csv', 6],
        '020': ['datasets/synthetic/scenario_2/020/scenario-2-%d-rcat-%d-icat.csv', 6],
        '041': ['datasets/synthetic/scenario_2/041/scenario-2-%d-rcat-%d-icat.csv', 6],
        '083': ['datasets/synthetic/scenario_2/083/scenario-2-%d-rcat-%d-icat.csv', 6],
        '166': ['datasets/synthetic/scenario_2/166/scenario-2-%d-rcat-%d-icat.csv', 6],
    }
}