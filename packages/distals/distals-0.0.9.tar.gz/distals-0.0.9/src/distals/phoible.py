import csv

def collect(all_data, data_folder, langname_utils):
    print('Reading Phoible')
    lang_data ={}
    with open(data_folder + '/phoible.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first = True
        for row in reader:
            if first:
                first = False
            iso_code = langname_utils.toISO(row[2], False)
            if iso_code == None:
                continue
            dialect = row[4]
            glyph_id = row[5]
            dialect = row[4]
            if iso_code not in lang_data:
                lang_data[iso_code] = {}
            if dialect not in lang_data[iso_code]:
                lang_data[iso_code][dialect] = set()
            lang_data[iso_code][dialect].add(glyph_id)
    for iso_code in lang_data:
        dialects = [x for x in lang_data[iso_code]]
        if len(dialects) == 1:
            dialect = dialects[0]
        elif 'NA' in dialects:
            dialect = 'NA'
        else:
            continue
        all_data[iso_code]['phoible'] = lang_data[iso_code][dialect]
    return all_data


def distance_metric(info1, info2, key):
    all_glyphs = info1.union(info2)
    if len(all_glyphs) == 0:
        return 0.0
    overlap = info1.intersection(info2)
    return 1- len(overlap)/len(all_glyphs)

