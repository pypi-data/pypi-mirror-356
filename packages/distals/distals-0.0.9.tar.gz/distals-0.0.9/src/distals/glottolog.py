import os
import configparser
from math import radians, degrees, sin, cos, asin, acos, sqrt

completeAES = {'extinct': '0. extinct', 'nearly extinct': '1. nearly extinct', 'moribund': '2. moribund', 'shifting': '3. shifting', 'threatened': '4. threatened', 'not endangered': '5. not endangered'}

def collect(all_data, data_folder, langname_utils):
    print('Reading info from Glottolog')
    for (root,dirs,files) in os.walk(data_folder + 'glottolog/languoids/tree/',topdown=True):
        for file in files:
            if not file.endswith('ini'):
                continue
            config = configparser.ConfigParser(interpolation=None)
            try:
                config.read(root + '/' + file)
                if 'iso639-3' not in config['core']:
                    continue
                iso639_code = langname_utils.toISO(config['core']['iso639-3'], False)
                if iso639_code == None: # invalid code used
                    continue

                if 'endangerment' in config:
                    aes = completeAES[config['endangerment']['status']]
                    all_data[iso639_code]['AES'] = aes
                if 'latitude' in config['core']:
                    lat = float(config['core']['latitude'])
                    long = float(config['core']['longitude'])
                    all_data[iso639_code]['loc'] = (long, lat)
            except:
                print('error in ' + root + '/' + file)
                continue
    return all_data 

def distance_metric(info1, info2, key):
    if key == 'AES':
        cat1 = int(info1[:1])
        cat2 = int(info2[:1])
        # assume values between 0 and 5 for normalization to 0-1.0
        dist = abs(cat1-cat2)
        return dist/5

    elif key == 'loc':
        lon1 = info1[0]
        lat1 = info1[1]
        lon2 = info2[0]
        lat2 = info2[1]
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        try:
            return (6371 * (
                acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
            )) / 20000 # 200000 is the maximum value, so we can normalize with this
        except ValueError:
            return None
    
