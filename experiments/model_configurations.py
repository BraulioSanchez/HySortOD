import os

def random_ranking(command):
    b = 5
    minSplit = 100
    cmd = 'echo "%s,0.5,0,%d,%d" >> code/results/HySortOD.csv' % (command[3], b, minSplit)
    os.system(cmd)

def configuration_hysortod_search(command):
    minSplit = 100
    for b in range(2, 100+1):
        cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], b, minSplit)
        os.system(cmd)

def configuration_hysortod_best_fixed(command):
    b = 5
    minSplit = 100
    cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], b, minSplit)
    os.system(cmd)

def configuration_iforest_search(command):
    for h in range(100, 300+1, 50):
        ψs = [2**i for i in range(5,10+1)]
        for ψ in ψs:
            cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], h, ψ)
            os.system(cmd)

def configuration_iforest_best_fixed(command):
    h = 100
    ψ = 250
    cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], h, ψ)
    os.system(cmd)

def configuration_hdoutliers_search(command):
    for alpha in [x / 100.0 for x in range(5, 51, 1)]:
        cmd = 'sh %s %s %d %s %.4f' % (command[0], command[1], command[2], command[3], alpha)
        os.system(cmd)

def configuration_knnoutlier(command):
    if 'glass' == command[3]:
        for k in range(1, 20+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'parkinson,ionosphere,breastw,thyroid'.__contains__(command[3]):
        for k in range(1, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'pima' == command[3]:
        for k in range(100, 500+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'satimage2' == command[3]:
        for k in range(1, 100+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'mammography' == command[3]:
        for k in range(10, 25+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*10)
            os.system(cmd)
    elif 'shuttle' == command[3]:
        for k in range(20, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*100)
            os.system(cmd)
    elif 'http' == command[3]:
        for k in range(20, 40+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*100)
            os.system(cmd)

def configuration_knnoutlier_best_fixed(command):
    k = 10
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
        os.system(cmd)

def configuration_dbout_search(command):
    if 'parkinson,glass,ionosphere,breastw,thyroid'.__contains__(command[3]):
        for d in range(1, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
            os.system(cmd)
    elif 'pima' == command[3]:
        for d in range(10, 200+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
            os.system(cmd)
    elif 'satimage2' == command[3]:
        for d in range(1, 20+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d*10)
            os.system(cmd)
    elif 'mammography' == command[3]:
        for d in range(1, 10+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
            os.system(cmd)
    elif 'shuttle' == command[3]:
        for d in range(1000, 3000+1, 50):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
            os.system(cmd)
    elif 'http' == command[3]:
        for d in range(1000, 3000+1, 50):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
            os.system(cmd)

def configuration_dbout_best_fixed(command):
    d = 50
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], d)
        os.system(cmd)

def configuration_lof_search(command):
    if 'parkinson,glass,ionosphere,breastw'.__contains__(command[3]):
        for k in range(1, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'pima' == command[3]:
        for k in range(100, 500+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'thyroid' == command[3]:
        for k in range(50, 150+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'satimage2' == command[3]:
        for k in range(50, 150+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'mammography' == command[3]:
        for k in range(100, 250+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'shuttle' == command[3]:
        for k in range(20, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*100)
            os.system(cmd)
    elif 'http' == command[3]:
        for k in range(20, 40+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*100)
            os.system(cmd)

def configuration_lof_best_fixed(command):
    k = 50
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
        os.system(cmd)

def configuration_odin_search(command):
    if 'parkinson,glass,ionosphere,breastw'.__contains__(command[3]):
        for k in range(1, 50+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'pima' == command[3]:
        for k in range(1, 300+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'thyroid' == command[3]:
        for k in range(1, 100+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'satimage2' == command[3]:
        for k in range(1, 200+1):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k*10)
            os.system(cmd)
    elif 'mammography' == command[3]:
        for k in range(100, 2000+1, 50):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'shuttle' == command[3]:
        for k in range(1000, 12000+1, 100):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)
    elif 'http' == command[3]:
        for k in range(2000, 7000+1, 100):
            cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
            os.system(cmd)

def configuration_odin_best_fixed(command):
    k = 50
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d' % (command[0], command[1], command[2], command[3], k)
        os.system(cmd)

def configuration_hilout_search(command):
    if 'parkinson' == command[3]:
        for k in range(1, 10+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'glass' == command[3]:
        for k in range(1, 100+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'ionosphere' == command[3]:
        for k in range(1, 20+1):
            for h in range(2, 50+1, 2):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'breastw' == command[3]:
        for k in range(1, 20+1):
            for h in range(2, 32+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'pima' == command[3]:
        for k in range(100, 500+1, 10):
            for h in range(1, 20+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'thyroid' == command[3]:
        for k in range(1, 20+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'satimage2' == command[3]:
        for k in range(1, 50+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'mammography' == command[3]:
        for k in range(1, 50+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'shuttle' == command[3]:
        for k in range(1, 20+1):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)
    elif 'http' == command[3]:
        for k in range(10, 300+1, 10):
            for h in range(1, 64+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
                os.system(cmd)

def configuration_hilout_best_fixed(command):
    k = 50
    h = 32
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], k, h)
        os.system(cmd)

def configuration_aloci_search(command):
    if 'parkinson' == command[3]:
        for n in range(1, 10+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'glass' == command[3]:
        for n in range(1, 200+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'ionosphere' == command[3]:
        for n in range(1, 50+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'breastw' == command[3]:
        for n in range(1, 10+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'pima' == command[3]:
        for n in range(1, 100+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'thyroid' == command[3]:
        for n in range(1, 50+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'satimage2' == command[3]:
        for n in range(1, 10+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'mammography' == command[3]:
        for n in range(1, 10+1):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'shuttle' == command[3]:
        for n in range(1, 3001+1, 100):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)
    elif 'http' == command[3]:
        for n in range(1, 5001+1, 100):
            for g in range(1, 4+1):
                cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
                os.system(cmd)

def configuration_aloci_best_fixed(command):
    n = 20
    g = 20
    for _ in range(10):
        cmd = 'sh %s %s %d %s %d %d' % (command[0], command[1], command[2], command[3], n, g)
        os.system(cmd)

def configuration_abod_search(command):
    cmd = 'sh %s %s %d %s' % (command[0], command[1], command[2], command[3])
    os.system(cmd)

def configuration_abod_best_fixed(command):
    cmd = 'sh %s %s %d %s' % (command[0], command[1], command[2], command[3])
    os.system(cmd)

configurations = {
    'hysortod': {
        # ----------- numerical
        'parkinson': configuration_hysortod_search,
        'glass': configuration_hysortod_search,
        'ionosphere': configuration_hysortod_search,
        'breastw': configuration_hysortod_search,
        'pima': configuration_hysortod_search,
        'thyroid': configuration_hysortod_search,
        'satimage2': configuration_hysortod_search,
        'mammography': configuration_hysortod_search,
        'shuttle': configuration_hysortod_search,
        'http': configuration_hysortod_search,
        # # ----------- categorical
        'hepatitis': configuration_hysortod_search,
        'tae': configuration_hysortod_search,
        'lymphography': configuration_hysortod_search,
        'heart': configuration_hysortod_search,
        'ecoli': configuration_hysortod_search,
        'crx': configuration_hysortod_search,
        'australian': configuration_hysortod_search,
        'anneal': configuration_hysortod_search,
        'german': configuration_hysortod_search,
        'cmc': configuration_hysortod_search,
        'car': configuration_hysortod_search,
        'nursery': configuration_hysortod_search,
        'adult': configuration_hysortod_search,
        'poker_hand': configuration_hysortod_search,
    },
    'iforest': {
        # ----------- numerical
        'parkinson': configuration_iforest_search,
        'glass': configuration_iforest_search,
        'ionosphere': configuration_iforest_search,
        'breastw': configuration_iforest_search,
        'pima': configuration_iforest_search,
        'thyroid': configuration_iforest_search,
        'satimage2': configuration_iforest_search,
        'mammography': configuration_iforest_search,
        'shuttle': configuration_iforest_search,
        'http': configuration_iforest_search,
        # ----------- categorical
        'hepatitis': configuration_iforest_search,
        'tae': configuration_iforest_search,
        'lymphography': configuration_iforest_search,
        'heart': configuration_iforest_search,
        'ecoli': configuration_iforest_search,
        'crx': configuration_iforest_search,
        'australian': configuration_iforest_search,
        'anneal': configuration_iforest_search,
        'german': configuration_iforest_search,
        'cmc': configuration_iforest_search,
        'car': configuration_iforest_search,
        'nursery': configuration_iforest_search,
        'adult': configuration_iforest_search,
        'poker_hand': configuration_iforest_search
    },
    'htoutliers': {
        # ----------- numerical
        'parkinson': configuration_hdoutliers_search,
        'glass': configuration_hdoutliers_search,
        'ionosphere': configuration_hdoutliers_search,
        'breastw': configuration_hdoutliers_search,
        'pima': configuration_hdoutliers_search,
        'thyroid': configuration_hdoutliers_search,
        'satimage2': configuration_hdoutliers_search,
        'mammography': configuration_hdoutliers_search,
        'shuttle': configuration_hdoutliers_search,
        'http': configuration_hdoutliers_search,
        # ----------- categorical
        'hepatitis': configuration_hdoutliers_search,
        'tae': configuration_hdoutliers_search,
        'lymphography': configuration_hdoutliers_search,
        'heart': configuration_hdoutliers_search,
        'ecoli': configuration_hdoutliers_search,
        'crx': configuration_hdoutliers_search,
        'australian': configuration_hdoutliers_search,
        'anneal': configuration_hdoutliers_search,
        'german': configuration_hdoutliers_search,
        'cmc': configuration_hdoutliers_search,
        'car': configuration_hdoutliers_search,
        'nursery': configuration_hdoutliers_search,
        'adult': configuration_hdoutliers_search,
        'poker_hand': configuration_hdoutliers_search
    },
    'hilout': {
        # ----------- numerical
        'parkinson': configuration_hilout_search,
        'glass': configuration_hilout_search,
        'ionosphere': configuration_hilout_search,
        'breastw': configuration_hilout_search,
        'pima': configuration_hilout_search,
        'thyroid': configuration_hilout_search,
        'satimage2': configuration_hilout_search,
        'mammography': configuration_hilout_search,
        'shuttle': configuration_hilout_search,
        'http': configuration_hilout_search,
    },
    'knnoutlier': {
        # ----------- numerical
        'parkinson': configuration_knnoutlier,
        'glass': configuration_knnoutlier,
        'ionosphere': configuration_knnoutlier,
        'breastw': configuration_knnoutlier,
        'pima': configuration_knnoutlier,
        'thyroid': configuration_knnoutlier,
        'satimage2': configuration_knnoutlier,
        'mammography': configuration_knnoutlier,
        'shuttle': configuration_knnoutlier,
        'http': configuration_knnoutlier,
    },
    'dbout': {
        # ----------- numerical
        'parkinson': configuration_dbout_search,
        'glass': configuration_dbout_search,
        'ionosphere': configuration_dbout_search,
        'breastw': configuration_dbout_search,
        'pima': configuration_dbout_search,
        'thyroid': configuration_dbout_search,
        'satimage2': configuration_dbout_search,
        'mammography': configuration_dbout_search,
        'shuttle': configuration_dbout_search,
        'http': configuration_dbout_search,
    },
    'lof': {
        # ----------- numerical
        'parkinson': configuration_lof_search,
        'glass': configuration_lof_search,
        'ionosphere': configuration_lof_search,
        'breastw': configuration_lof_search,
        'pima': configuration_lof_search,
        'thyroid': configuration_lof_search,
        'satimage2': configuration_lof_search,
        'mammography': configuration_lof_search,
        'shuttle': configuration_lof_search,
        'http': configuration_lof_search,
    },
    'odin': {
        # ----------- numerical
        'parkinson': configuration_odin_search,
        'glass': configuration_odin_search,
        'ionosphere': configuration_odin_search,
        'breastw': configuration_odin_search,
        'pima': configuration_odin_search,
        'thyroid': configuration_odin_search,
        'satimage2': configuration_odin_search,
        'mammography': configuration_odin_search,
        'shuttle': configuration_odin_search,
        'http': configuration_odin_search,
    },
    'aloci': {
        # ----------- numerical
        'parkinson': configuration_aloci_search,
        'glass': configuration_aloci_search,
        'ionosphere': configuration_aloci_search,
        'breastw': configuration_aloci_search,
        'pima': configuration_aloci_search,
        'thyroid': configuration_aloci_search,
        'satimage2': configuration_aloci_search,
        'mammography': configuration_aloci_search,
        'shuttle': configuration_aloci_search,
        'http': configuration_aloci_search,
    },
    'abod': {
        # ----------- numerical
        'parkinson': configuration_abod_search,
        'glass': configuration_abod_search,
        'ionosphere': configuration_abod_search,
        'breastw': configuration_abod_search,
        'pima': configuration_abod_search,
        'thyroid': configuration_abod_search,
        'satimage2': configuration_abod_search,
        'mammography': configuration_abod_search,
        'shuttle': configuration_abod_search,
        'http': configuration_abod_search,
    }
}

configurations_scalability = {
    'hysortod': {
        'http': configuration_hysortod_best_fixed,
        'poker_hand': configuration_hysortod_best_fixed,
    },
    'iforest': {
        'http': configuration_iforest_best_fixed,
        'poker_hand': configuration_iforest_best_fixed
    },
    'hilout': {
        'http_without_header': configuration_hilout_best_fixed,
    },
    'knnoutlier': {
        'http_without_header': configuration_knnoutlier_best_fixed,
    },
    'dbout': {
        'http_without_header': configuration_dbout_best_fixed,
    },
    'lof': {
        'http_without_header': configuration_lof_best_fixed,
    },
    'odin': {
        'http_without_header': configuration_odin_best_fixed,
    },
    'aloci': {
        'http_without_header': configuration_aloci_best_fixed,
    },
    'abod': {
        'http_without_header': configuration_abod_best_fixed,
    }
}

configurations_categorical = {
    'hysortod': {
        'hepatitis-con': configuration_hysortod_best_fixed,
        'tae-con': configuration_hysortod_best_fixed,
        'lymphography-con': configuration_hysortod_best_fixed,
        'heart-con': configuration_hysortod_best_fixed,
        'ecoli-con': configuration_hysortod_best_fixed,
        'crx-con': configuration_hysortod_best_fixed,
        'australian-con': configuration_hysortod_best_fixed,
        'anneal-con': configuration_hysortod_best_fixed,
        'german-con': configuration_hysortod_best_fixed,
        'cmc-con': configuration_hysortod_best_fixed,
        'car-con': random_ranking,
        'nursery-con': random_ranking,
        'adult-con': configuration_hysortod_best_fixed,
        'poker_hand-con': random_ranking
    }
}