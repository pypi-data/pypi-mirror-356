
# String distances from the AsjpDist-full program
# @author: rarakar
def levenshtein(a,b):
    UNNORM = False
    m=[];la=len(a)+1;lb=len(b)+1
    for i in range(0,la):
        m.append([])
        for j in range(0,lb):m[i].append(0)
        m[i][0]=i
    for i in range(0,lb):m[0][i]=i
    for i in range(1,la):
        for j in range(1,lb):
            s=m[i-1][j-1]
            if (a[i-1]!=b[j-1]):s=s+1
            m[i][j]=min(m[i][j-1]+1,m[i-1][j]+1,s)
    la=la-1;lb=lb-1
    if UNNORM:
        return float(m[la][lb])
    return float(m[la][lb])/float(max(la,lb))

def expand_list(data):
    new_data = [None] * 100
    for item in data:
        new_data[int(item[0])-1] = item[-1]
    return new_data


def collect(all_data, data_folder, langname_utils):
    aspj_lines = open(data_folder + 'lists.txt', encoding='ISO-8859-1').readlines()
    for lineIdx, line in enumerate(aspj_lines):
        if line[0].isupper() and '{' in line:

            lang_name = line.split('{')[0]
            lang_code = aspj_lines[lineIdx+1].strip().split(' ')[-1]
            lang_code = langname_utils.toISO(lang_code, False)
            lang_code2 = langname_utils.name_to_iso(lang_name.lower().replace('_', ' '))
            if lang_code == None and lang_code2 == None:
                continue
            if lang_code == None and lang_code2 != None:
                lang_code = lang_code2
            lang_code = langname_utils.toISO(lang_code, False)
            if lang_code == None:
                continue

            data = []
            for i in range(100):
                if aspj_lines[lineIdx+2+i][0].isdigit():
                    line = aspj_lines[lineIdx+2+i].strip().replace(' //', '')
                    tok = line.split()
                    num = tok[0]
                    en = tok[1]
                    asjp_info = ' '.join(tok[2:])
                    data.append([num, asjp_info.split(', ')])
                else:
                    break

            all_data[lang_code]['asjp'] = data
    return all_data

def distance_metric(data1, data2, key):
    data1 = expand_list(data1)
    data2 = expand_list(data2)
    dists = [[None]*100 for _ in range(100)]
    for idx1, item1 in enumerate(data1):
        for idx2, item2 in enumerate(data2):
            if None not in [item1, item2]:
                all_dists = []
                for item1_alternative in item1:
                    for item2_alternative in item2:
                        all_dists.append(levenshtein(item1_alternative, item2_alternative))
                dists[idx1][idx2] = min(all_dists)#sum(all_dists)/len(all_dists)

    # get average over all non-matching pairs to normalize for chance
    all_dists = []
    for x in range(100):
        for y in range(100):
            if x != y and dists[x][y] != None:
                all_dists.append(dists[x][y])
    avg_dist = sum(all_dists)/len(all_dists)
    
    all_ldnd = []
    for item in range(100):
        if dists[item][item] != None:
            ldn = dists[item][item]
            ldnd = ldn/avg_dist
            all_ldnd.append(ldnd)
    return (sum(all_ldnd)/len(all_ldnd)) / 2

