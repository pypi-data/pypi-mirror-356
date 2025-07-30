
def collect(all_data, data_folder, langname_utils):
    print('Reading GlotScript')
    glotscripts = {}
    for line in open('data/GlotScript.tsv').readlines()[1:]:
        tok = line.strip().lower().split('\t')
        if len(tok) > 1:
            lang = langname_utils.toISO(tok[0], False)
            if lang != None:
                scripts = set([x.strip() for x in tok[1].split(',')])
                glotscripts[lang] = scripts

    print('Reading Linguameta')
    for line in open(data_folder + 'linguameta.tsv').readlines()[1:]:
        tok = line.strip().lower().split('\t')
        if len(tok) > 1:
            scripts =  set([x.strip() for x in tok[1].split(',') if x != ' brai'])
            speakers = tok[4]
            scripts = tok[5].split(', ')
            iso_code = langname_utils.toISO(tok[1], False)
            if iso_code == None:
                continue
            if speakers != '':
                all_data[iso_code]['speakers'] = int(speakers)
            if scripts != ['']:
                # Merging scripts from both sources
                # if both have a different set, only take intersection
                # if there is no intersection, just take linguameta
                if iso_code in glotscripts:
                    int_scripts = set(scripts).intersection(glotscripts[iso_code])
                    if len(int_scripts) == 0:
                        int_scripts = set(scripts)
                else:
                    int_scripts = set(scripts)
                all_data[iso_code]['scripts'] = int_scripts
    return all_data


def distance_metric(info1, info2, key):
    if key == 'scripts':
        all_scripts = info1.union(info2)
        if len(all_scripts) == 0:
            return 0.0
        overlap = info1.intersection(info2)
        return 1- len(overlap)/len(all_scripts)

    elif key == 'speakers':
        if max(info1, info2) == 0:
            return 1
        return 1 - min(info1, info2)/ max(info1, info2)

