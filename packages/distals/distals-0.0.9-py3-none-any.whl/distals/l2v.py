from scipy.spatial import distance
import numpy as np

def collect(all_data, data_folder, langname_utils):
    import lang2vec.lang2vec as l2v
    # Add lang2vec data
    print('Getting lang2vec data')
    values = 'syntax_average+phonology_average+inventory_average'
    for lang_code in all_data:
        if lang_code in l2v.LANGUAGES:
            feats = l2v.get_features(lang_code, values)[lang_code]
            all_data[lang_code]['lang2vec'] = [float(x) if type(x) == np.float64 else x for x in feats]

    values = 'syntax_knn+phonology_knn+inventory_knn'
    for lang_code in all_data:
        if lang_code in l2v.LANGUAGES:
            feats = l2v.get_features(lang_code, values)[lang_code]
            all_data[lang_code]['lang2vec_knn'] = [float(x) if type(x) == np.float64 else x for x in feats]
    return all_data

def distance_metric(lang1_data, lang2_data, key):
    langvec1_subset = []
    langvec2_subset = []
    for featval1, featval2 in zip(lang1_data, lang2_data):
        if '--' not in [featval1, featval2]:
            langvec1_subset.append(featval1)
            langvec2_subset.append(featval2)
    if len(langvec1_subset) == 0:
        return -1
    # Suppress warnings, because there are some, but the results are correct
    with np.errstate(invalid='ignore'):
        return distance.cosine(langvec1_subset, langvec2_subset)


