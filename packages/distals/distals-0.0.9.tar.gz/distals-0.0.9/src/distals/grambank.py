import os
import csv
import math
from sklearn.metrics.pairwise import nan_euclidean_distances

groupings = {'grambank': ['GB303', 'GB149', 'GB070', 'GB071', 'GB408', 'GB409', 'GB410', 'GB074', 'GB075', 'GB080', 'GB081', 'GB079', 'GB092', 'GB093', 'GB089', 'GB090', 'GB091', 'GB094', 'GB098', 'GB095', 'GB096', 'GB105', 'GB072', 'GB073', 'GB108', 'GB027', 'GB103', 'GB104', 'GB026', 'GB069', 'GB059', 'GB430', 'GB431', 'GB432', 'GB433', 'GB313', 'GB058', 'GB155', 'GB156', 'GB028', 'GB301', 'GB265', 'GB270', 'GB273', 'GB275', 'GB276', 'GB266', 'GB146', 'GB020', 'GB022', 'GB021', 'GB023', 'GB035', 'GB037', 'GB036', 'GB151', 'GB038', 'GB159', 'GB160', 'GB158', 'GB048', 'GB049', 'GB047', 'GB321', 'GB051', 'GB052', 'GB054', 'GB192', 'GB196', 'GB197', 'GB053', 'GB170', 'GB171', 'GB172', 'GB314', 'GB315', 'GB296', 'GB167', 'GB257', 'GB260', 'GB262', 'GB263', 'GB264', 'GB285', 'GB286', 'GB291', 'GB324', 'GB326', 'GB325', 'GB116', 'GB177', 'GB057', 'GB188', 'GB187', 'GB046', 'GB316', 'GB317', 'GB318', 'GB319', 'GB320', 'GB039', 'GB165', 'GB166', 'GB041', 'GB043', 'GB109', 'GB184', 'GB185', 'GB186', 'GB044', 'GB042', 'GB302', 'GB304', 'GB099', 'GB031', 'GB030', 'GB400', 'GB415', 'GB132', 'GB118', 'GB131', 'GB136', 'GB522', 'GB133', 'GB150', 'GB122', 'GB123', 'GB140', 'GB256', 'GB253', 'GB254', 'GB252', 'GB135', 'GB134', 'GB068', 'GB117', 'GB333', 'GB334', 'GB335', 'GB336', 'GB204', 'GB198', 'GB115', 'GB114', 'GB327', 'GB328', 'GB329', 'GB330', 'GB331', 'GB421', 'GB422', 'GB086', 'GB120', 'GB520', 'GB322', 'GB323', 'GB139', 'GB297', 'GB119', 'GB312', 'GB519', 'GB138', 'GB107', 'GB137', 'GB298', 'GB299', 'GB152', 'GB084', 'GB309', 'GB521', 'GB082', 'GB083', 'GB121', 'GB110', 'GB111', 'GB148', 'GB113', 'GB147', 'GB305', 'GB306', 'GB124', 'GB401', 'GB129', 'GB127', 'GB126', 'GB250', 'GB402', 'GB403', 'GB300', 'GB024a', 'GB024b', 'GB025a', 'GB025b', 'GB065a', 'GB065b', 'GB130a', 'GB130b', 'GB193a', 'GB193b', 'GB203a', 'GB203b'], 'gb_clause': ['GB303', 'GB105', 'GB027', 'GB156', 'GB301', 'GB265', 'GB270', 'GB273', 'GB275', 'GB276', 'GB266', 'GB257', 'GB260', 'GB262', 'GB263', 'GB264', 'GB285', 'GB286', 'GB291', 'GB324', 'GB326', 'GB302', 'GB304', 'GB132', 'GB131', 'GB136', 'GB522', 'GB133', 'GB150', 'GB140', 'GB256', 'GB253', 'GB254', 'GB252', 'GB135', 'GB134', 'GB327', 'GB328', 'GB329', 'GB330', 'GB331', 'GB421', 'GB422', 'GB139', 'GB297', 'GB138', 'GB137', 'GB298', 'GB299', 'GB152', 'GB130a', 'GB130b'], 'gb_verbal_domain': ['GB149', 'GB080', 'GB081', 'GB079', 'GB092', 'GB093', 'GB089', 'GB090', 'GB091', 'GB094', 'GB098', 'GB095', 'GB096', 'GB108', 'GB103', 'GB104', 'GB155', 'GB146', 'GB151', 'GB158', 'GB116', 'GB177', 'GB109', 'GB099', 'GB400', 'GB118', 'GB122', 'GB123', 'GB117', 'GB115', 'GB114', 'GB086', 'GB120', 'GB520', 'GB322', 'GB323', 'GB119', 'GB312', 'GB519', 'GB107', 'GB084', 'GB309', 'GB521', 'GB082', 'GB083', 'GB121', 'GB110', 'GB111', 'GB148', 'GB113', 'GB147', 'GB124', 'GB401', 'GB129', 'GB127', 'GB126', 'GB402', 'GB403', 'GB300'], 'gb_nominal_domain': ['GB070', 'GB408', 'GB409', 'GB410', 'GB074', 'GB075', 'GB072', 'GB026', 'GB069', 'GB059', 'GB430', 'GB431', 'GB432', 'GB433', 'GB058', 'GB020', 'GB022', 'GB021', 'GB023', 'GB035', 'GB037', 'GB036', 'GB038', 'GB159', 'GB160', 'GB048', 'GB049', 'GB047', 'GB321', 'GB051', 'GB052', 'GB054', 'GB192', 'GB053', 'GB170', 'GB171', 'GB172', 'GB314', 'GB315', 'GB296', 'GB325', 'GB057', 'GB188', 'GB187', 'GB046', 'GB316', 'GB317', 'GB318', 'GB319', 'GB320', 'GB039', 'GB165', 'GB166', 'GB041', 'GB043', 'GB184', 'GB185', 'GB186', 'GB044', 'GB042', 'GB068', 'GB204', 'GB198', 'GB250', 'GB024a', 'GB024b', 'GB025a', 'GB025b', 'GB065a', 'GB065b', 'GB193a', 'GB193b', 'GB203a', 'GB203b'], 'gb_pronoun': ['GB071', 'GB073', 'GB313', 'GB028', 'GB196', 'GB197', 'GB167', 'GB031', 'GB030', 'GB415', 'GB305', 'GB306'], 'gb_numeral': ['GB333', 'GB334', 'GB335', 'GB336']}
GB_MULTI_VALUE_FEATURES = ["GB024", "GB025", "GB065", "GB130", "GB193", "GB203"]

def collect(all_data, data_folder, langname_utils):
    print('Converting grambank')
    glot2iso = {}
    for (root,dirs,files) in os.walk(data_folder + 'glottolog/languoids/tree/',topdown=True):
        for file in files:
            iso = None
            for line in open(os.path.join(root, file), encoding='utf-8', errors='ignore'):
                if line.startswith('iso639-3 = '):
                    iso = line.strip().split(' ')[-1]
            if iso == None:
                continue
            lang_code = langname_utils.toISO(iso, False)
            if lang_code in all_data:
                glot_code = root.split('/')[-1]
                glot2iso[glot_code] = iso

    with open(data_folder + 'values.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first = True
        for row in reader:
            if first:
                first = False
                continue
            glot_code = row[1]
            if glot_code not in glot2iso:
                continue
            iso_code = langname_utils.toISO(glot2iso[glot_code], False)
                
            feat = row[2]
            val = row[3]
            if val == '?':
                continue
            if iso_code in all_data:
                if 'grambank' not in all_data[iso_code]:
                    all_data[iso_code]['grambank'] = {}
            
                if feat in GB_MULTI_VALUE_FEATURES:
                    all_data[iso_code]['grambank'][feat + 'a'] = int(feat == 1)
                    all_data[iso_code]['grambank'][feat + 'b'] = int(feat == 2)
                    if feat == 3:
                        all_data[iso_code]['grambank'][feat + 'a'] = 1
                        all_data[iso_code]['grambank'][feat + 'b'] = 1
                    if feat == 0:
                        all_data[iso_code]['grambank'][feat + 'a'] = 0
                        all_data[iso_code]['grambank'][feat + 'b'] = 0

                else: 
                    all_data[iso_code]['grambank'][feat] = int(val)

        total_len = len(groupings['grambank']) - len(GB_MULTI_VALUE_FEATURES)
        cutoff = int(total_len * .25)
        langs_to_remove = []
        for lang in all_data:
            if 'grambank' in all_data[lang] and len(all_data[lang]['grambank']) < cutoff:
                langs_to_remove.append(lang)
        for lang in langs_to_remove:
            del all_data[lang]['grambank']
                
    return all_data


def distance_metric(lang1_data, lang2_data, key):
    # Now filter for mutually present features
    langvec1 = []
    langvec2 = []
    for feat in groupings[key]:
        nan = float("NaN")
        if feat in lang1_data:
            langvec1.append(lang1_data[feat])
        else:
            langvec1.append(nan)

        if feat in lang2_data:
            langvec2.append(lang2_data[feat])
        else:
            langvec2.append(nan)

    total_size = len(groupings[key])
    norm_factor = math.sqrt(total_size)
    return nan_euclidean_distances([langvec1], [langvec2])[0][0]/norm_factor
    

    
