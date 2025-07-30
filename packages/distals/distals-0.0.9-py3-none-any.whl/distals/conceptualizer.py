import os

def collect(all_data, data_folder, langname_utils):
    data = open(data_folder + 'sim_matrix.csv').readlines()
    columns = data[0].split(',')
    for row in data[1:]:
        tok = row.split(',')
        lang1 = langname_utils.toISO(tok[0].strip(), False)
        if lang1 == None:
            continue
        dist_dict = {}
        for lang2, dist in zip(columns[1:], tok[1:]):
            lang2 = langname_utils.toISO(lang2.strip(), False)
            if lang2 != None:
                dist_dict[lang2] = float(dist)
        all_data[lang1]['concepts'] = dist_dict
    return all_data 

def distance_metric(lang1_dict, lang2code):
    if lang2code in lang1_dict:
        return 1-lang1_dict[lang2code]
    else:
        return -1
    

