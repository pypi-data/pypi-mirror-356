
def collect(all_data, data_folder, langname_utils):
    # Add wikipedia sizes
    print('Getting wiki sizes')
    for line in open(data_folder + 'List_of_Wikipedias.htm'):
        # TODO, this should be done in a more robust way
        if line.startswith('<table class="wikitable plainrowheaders'):
            for row in line.split('<th scope="row'):
                if 'Special:Statistics">' in row:
                    num_articles = row.split('Special:Statistics">')[1].split('<')[0].split('>')[-1]

                    lang_code1_old = None
                    if '<i lang="' in row:
                        lang_code1_old = row.split('<i lang="')[1].split('"')[0].split('<')[0].split('-')[0]
                    lang_code1 = langname_utils.toISO(lang_code1_old, False)
                    lang_code2_old = row.split('</a></code>')[1].split('>')[-1].split('-')[0]
                    lang_code2 = langname_utils.toISO(lang_code2_old, False)
                    codes = set([lang_code1, lang_code2])
                    if None in codes:
                        codes.remove(None)

                    #if len(codes) == 0:
                    #    print(lang_code1_old, lang_code2_old)
                    if lang_code2 != None:
                        all_data[lang_code2]['wiki_size'] = int(num_articles.replace(',', ''))
    # for language not seen yet, we also know:
    for lang_code in all_data:
        if 'wiki_size' not in all_data[lang_code]:
            all_data[lang_code]['wiki_size'] = 0
    return all_data


def distance_metric(lang1_size, lang2_size, key):
    if max(lang1_size, lang2_size) == 0:
        return 0.0
    return 1- min(lang1_size, lang2_size)/ max(lang1_size, lang2_size)
    
