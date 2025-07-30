import os
import csv
import math

def collect(all_data, data_folder, langname_utils):
    lang_mapping = {}
    with open(data_folder + 'wals/cldf/languages.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first = True
        for row in reader:
            if first:
                first = False
                continue
            lang_id = row[0]
            iso_code = row[6]
            lang_mapping[lang_id] = iso_code

    with open(data_folder + 'wals/cldf/values.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first = True
        for row in reader:
            if first:
                first = False
                continue
            lang = row[1]
            iso_code = langname_utils.toISO(lang_mapping[lang], False)
            if iso_code == None:
                continue
            if 'wals' not in all_data[iso_code]:
                all_data[iso_code]['wals'] = {}

            feat = row[2]
            val = row[3]
            all_data[iso_code]['wals'][feat] = val
   
    total = 192
    cutoff = int(total * .25)         
    for lang in all_data:
        if 'wals' in all_data[lang] and len(all_data[lang]['wals']) < cutoff:
            langs_to_remove.append(lang)
    for lang in langs_to_remove:
        del all_data[lang]['wals']
    return all_data


def distance_metric(lang1_data, lang2_data, key):
    # Unclear as there are multiple possible values (which are not continuous), percentage of overlap?
    return nan_euclidean_distances([langvec1], [langvec2])[0][0]/norm_factor

