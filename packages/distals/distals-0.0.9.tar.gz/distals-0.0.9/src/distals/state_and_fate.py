
group2name = {'0': '0. The Left-Behinds', '1': '1. The Scraping-Bys', '2': '2. The Hopefuls', '3': '3. The Rising Stars', '4': '4. The Underdogs', '5': '5. The Winners'}

def collect(all_data, data_folder, langname_utils):
    print("Getting state of languages")
    for line in open(data_folder + 'lang2tax.txt'):
        lang_name, group = line.strip().split(',')
        lang_code = langname_utils.name_to_iso(lang_name)
        if lang_code == None:
            continue
        all_data[lang_code]['nlp_state'] = group2name[group]

    return all_data


def distance_metric(label1, label2, key):
    cat1 = int(label1[:1])
    cat2 = int(label2[:1])
    # assume values between 0 and 5 for normalization to 0-1.0
    dist = abs(cat1-cat2)
    return dist/5
    
