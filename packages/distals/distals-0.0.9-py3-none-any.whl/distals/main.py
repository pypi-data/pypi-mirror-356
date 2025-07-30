#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import pickle
import os
import gzip
import pickle
import requests
import sys

from . import langname_utils

from . import wiki
from . import state_and_fate
from . import linguameta
from . import glottolog
from . import phoible
from . import l2v
from . import grambank
from . import glot_tree
from . import asjp
from . import conceptualizer
from . import textbased

average_positives = {'typology': ['grambank', 'phoible'], 'wordlists': ['asjp', 'concepts'], 'textbased': ['char_JSD', 'textcat'], 'metadata': ['wiki_size', 'nlp_state', 'scripts', 'speakers', 'glot_tree', 'AES']}

classes = [
    (wiki, 'wiki_size', 'metadata'),
    (state_and_fate, 'nlp_state', 'metadata'),
    (linguameta, 'speakers', 'metadata'),
    (glottolog, 'AES', 'metadata'),
    (glottolog, 'loc', 'metadata'),
    (l2v, 'lang2vec', 'typology'),
    (l2v, 'lang2vec_knn', 'typology'),
    (phoible, 'phoible', 'typology'),
    (grambank, 'grambank', 'typology'),
    (grambank, 'gb_clause', 'typology'),
    (grambank, 'gb_nominal_domain', 'typology'),
    (grambank, 'gb_numeral', 'typology'),
    (grambank, 'gb_pronoun', 'typology'),
    (grambank, 'gb_verbal_domain', 'typology'),
    (glot_tree, 'glot_tree', 'typology'),
    (linguameta, 'scripts', 'typology'),
    (asjp, 'asjp', 'wordlists'),
    (conceptualizer, 'concepts', 'wordlists'),
    (textbased, 'whitespace', 'textbased'),
    (textbased, 'punctuation', 'textbased'),
    (textbased, 'char_JSD', 'textbased'),
    (textbased, 'textcat', 'textbased')
]

keys = [x[1] for x in classes] 

def dict_to_str(data):
    if len(data) < 10:
        return str(data)
    first = list(data.keys())[:3]
    last = list(data.keys())[-3:]
    result = '{'
    for key in first:
        if type(data[key]) == float:
            result += "'" + key + "': {:.4f}".format(data[key]) + ', '
        else:
            result += "'" + key + "': " + str(data[key]) + ', '
    result += '..., '
    for key in last:
        if type(data[key]) == float:
            result += "'" + key + "': {:.4f}".format(data[key]) + ', '
        else:
            result += "'" + key + "': " + str(data[key]) + ', '
    return result[:-2] + '}'



class Distals():
    def __init__(self, 
                database_path: str = 'distals-db.pickle.gz'):
        self.all_data = {}
        self.langname_utils = None

        if os.path.isfile(database_path):
            print('loading from: ' + database_path, file=sys.stderr)
            with gzip.open(database_path, "rb") as f:
                self.all_data = pickle.load(f)
                self.langname_utils = pickle.load(f)
        else:
            print(database_path + ' not found, initializing database from scratch', file=sys.stderr)
            self.langname_utils = langname_utils.LangnameUtils()
            for line in open('data/iso-639-3.tab').readlines()[1:]:
                tok = line.strip().split('\t')
                if tok[4] == 'I':
                    self.all_data[tok[0]] = {'lang_name': tok[6]}

    def update_langnames(self, database_path: str, data_folder: str):
        print('Updating language names information to ' + database_path, file=sys.stderr)
        self.langname_utils = langname_utils.LangnameUtils()
        with gzip.open(database_path, 'wb') as f:
            pickle.dump(self.all_data, f)
            pickle.dump(self.langname_utils, f)

    def update_databases(self, database_path: str, data_folder: str):
        print('Updating features to ' + database_path, file=sys.stderr)
        # TODO call 0.update.sh, make data_folder being used
        # TODO, this doesnt take into account multiple features within the group (collects twice)
        # so we should make a mapping, so that we can remove full groups, and then look them up once
        class2feats = {}
        for python_class, name, group in classes:
            if group == 'textbased':
                continue
            if python_class not in class2feats:
                class2feats[python_class] = []
            class2feats[python_class].append(name)

        for python_class in class2feats:
            for feat_name in class2feats[python_class]:
            # remove old info
                for lang in self.all_data:
                    if feat_name in self.all_data[lang]:
                        del self.all_data[lang][feat_name]
            # add new info
            self.all_data = python_class.collect(self.all_data, data_folder, self.langname_utils)

        with gzip.open(database_path, "wb") as f:
            pickle.dump(self.all_data, f)
            pickle.dump(self.langname_utils, f)
        

    def update_textbased(self, database_path: str, data_folder: str):
        print('Updating textbased features to ' + database_path, file=sys.stderr)
        self.all_data = textbased.collect(self.all_data, data_folder, self.langname_utils)
        with gzip.open(database_path, "wb") as f:
            pickle.dump(self.all_data, f)
            pickle.dump(self.langname_utils, f)
        

    def report_distances(self, iso_code1, iso_code2):
        results = self.get_dists(iso_code1, iso_code2)
        print('=' * 40)
        print('Distances between ' + iso_code1 + ' and ' + iso_code2 + ' (-1 if the feature is not available for both)')
        for category in results:
            print(category.upper())
            for key in results[category]:
                print(key + ': {:.4f}'.format(results[category][key]))
            print()
    
    def report(self, iso_code):
        print('=' * 40)
        print('Information for ' + iso_code)
        for key in keys:
            if key.startswith('gb_'):
                continue
            if key in self.all_data[iso_code]:
                val = self.all_data[iso_code][key]
                if type(val) == list and len(val) > 10:
                    print(key + ': ' + str(val[:3])[:-1] + ', ..., ' + str(val[-3:])[1:])
                elif type(val) == set and len(val) > 10:
                    val = list(sorted(val))
                    print(key + ': ' + str(val[:3])[:-1] + ', ..., ' + str(val[-3:])[1:])
                elif key in ['grambank', 'char_JSD']:
                    print(key + ': ' + dict_to_str(val))
                elif type(val) == dict:
                    continue
                elif type(val) == int and val > 999:
                    print(key + ': {0:,}'.format(val))
                elif type(val) == float:
                    print(key + ': {:.6f}'.format(val))
                else:
                    print(key + ': ' + str(val))
            else:
                print(key + ': None')
        print()
    
    def get_dists(self, lang1, lang2, aslist=False):
        lang1 = self.langname_utils.toISO(lang1)
        lang2 = self.langname_utils.toISO(lang2)
        result = {}
        result_list = []
        for clas_idx in range(len(classes)):
            key = classes[clas_idx][1]
            cat_class = classes[clas_idx][0]
            if cat_class == grambank:
                if 'grambank' not in self.all_data[lang1] or 'grambank' not in self.all_data[lang2]:
                    dist = -1
                else:
                    dist = cat_class.distance_metric(self.all_data[lang1]['grambank'], self.all_data[lang2]['grambank'], key)
            elif key not in self.all_data[lang1] or key not in self.all_data[lang2]:
                dist = -1
            elif key == 'concepts':
                dist = cat_class.distance_metric(self.all_data[lang1][key], lang2)
            else:
                dist = cat_class.distance_metric(self.all_data[lang1][key], self.all_data[lang2][key], key)
            if dist == None: # where does this happen?
                dist = -1
        
            result_list.append(float(dist))
            category = classes[clas_idx][2]
            if category not in result:
                result[category] = {}
            result[category][key] = float(dist)
    
        avgs_list = []
        for category in result:
            scores = []
            for feature in result[category]:
                if feature in average_positives[category] and result[category][feature] != -1:
                    scores.append(result[category][feature])
            if len(scores) == 0:
                result[category]['average'] = -1
                avgs_list.append(-1)
            else:
                result[category]['average'] = sum(scores)/len(scores)
                avgs_list.append(sum(scores)/len(scores))
        if aslist:
            return result_list, avgs_list
        return result

    def get_coverage(self):
        counts = {key: 0 for key in keys if not key.startswith('gb_')}
        for lang in self.all_data:
            for key in self.all_data[lang]:
                if key == 'lang_name' or key.startswith('gb_'):
                    continue
                counts[key] += 1
        return counts

    def name_to_iso(self, lang):
        return self.langname_utils.name_to_iso(lang)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang1", required=False,
                    help="ISO-639-3 code of a language. When no lang2 is specified, just prints the information for this language.")
    parser.add_argument("--lang2", required=False,
                    help="ISO-639-3 code for the second language of the language pair. If it is used, we will also show distances between the two languages")    
    parser.add_argument("--langs", required=False, nargs='+',
                    help="List of languages, for which we will generate a confusion matrix for each language.")

    parser.add_argument("--database_path", required=False,
                    help="Path to the database that stores the information, if one of the update commands is used, this will be the path where the updates will be stored")
    parser.add_argument("--update_langnames", action="store_true",
                    help="Collect language names and codes")
    parser.add_argument("--update_databases", action="store_true",
                    help="Update the databases to extract features from.")
    parser.add_argument("--update_textbased", action="store_true",
                    help="Update the text based features, note that you should download the LTI-langID corpus first.")

    parser.add_argument("--coverage", action="store_true",
                    help="Print the coverage of features (after potential updates)")

    args = parser.parse_args()


    database_path = args.database_path
    if database_path == None:
        print('database_path not defined, searching for database in:', file=sys.stderr)
        print('current folder', file=sys.stderr)
        if os.path.isfile('./distals-db.pickle.gz'):
            database_path = './distals-db.pickle.gz'
        else:
            print('.cache', file=sys.stderr)
            if 'HOME' in os.environ:
                cache_dir = os.path.join(os.environ['HOME'], '.cache', 'distals') + '/'
                if os.path.isfile(os.path.join(cache_dir, './distals-db.pickle.gz')):
                    database_path = os.path.join(cache_dir, './distals-db.pickle.gz')
                if not os.path.isdir(cache_dir):
                    os.makedirs(cache_dir)
                download_dir = cache_dir
            else:
                download_dir = '.'
        if database_path == None:        
            print('Database not found, saving a recent copy in: ' + download_dir, file=sys.stderr)
            print("If you want to start from scratch instead, just use --database_path to a non-existing path")
            myfile = requests.get('https://bitbucket.org/robvanderg/lang_dist/raw/6761423798dfd86e874d0cff5dbb889ac8f0c94c/distals-db.pickle.gz')
            gzip.open(download_dir + 'distals-db.pickle.gz', 'wb').write(myfile.content)
            database_path = download_dir + 'distals-db.pickle.gz'
 
    main_model = Distals(database_path)

    if args.update_langnames:
        main_model.update_langnames(database_path, 'data/')

    if args.update_databases:
        main_model.update_databases(database_path, 'data/')
        
    if args.update_textbased:
        main_model.update_textbased(database_path, 'data/MILTALE-CLEAN/')


        
    print(str(len(main_model.all_data)) +  " languages loaded", file=sys.stderr)
    if args.coverage:
        counts = main_model.get_coverage()
        for key in counts:
            print(key + ': ' + str(counts[key]))
        print()

    if args.lang1:
        language1 = main_model.langname_utils.toISO(args.lang1, True)
        if language1 == None:
            print('Error ' + language1 + ' ISO-639-3 code not found.')
            exit(1)
        main_model.report(language1)

        if args.lang2 != None:
            language2 = main_model.langname_utils.toISO(args.lang2, True)
            if language2 == None:
                print('Error ' + language2 + ' ISO-639-3 code not found.')
                exit(1)

            main_model.report(language2)

            main_model.report_distances(language1, language2)

    if args.langs:
        import pandas as pd
        pd.options.display.float_format = '{:.4f}'.format
        if len(args.langs) < 3:
            print('--langs is supposed to be used with at least 3 languages')
        iso_codes = []
        for lang in args.langs:
            iso_code = main_model.langname_utils.toISO(lang, True)
            if iso_code == None:
                print('Error ' + lang + ' ISO-639-3 code not found.')
                exit(1)
            iso_codes.append(iso_code)
            main_model.report(iso_code)

        coarse_data = {}
        fine_data = {}
        for src_lang_idx, src_lang in enumerate(iso_codes):
            for tgt_lang_idx, tgt_lang in enumerate(iso_codes):
                if src_lang == tgt_lang:
                    continue
                dists = main_model.get_dists(src_lang, tgt_lang)
                for cat in dists:
                    if cat not in coarse_data:
                        coarse_data[cat] = [[0.0] * len(iso_codes) for _ in range(len(iso_codes))]
                    coarse_data[cat][src_lang_idx][tgt_lang_idx] = dists[cat]['average']
                    for fine_cat in dists[cat]:
                        if fine_cat == 'average':
                            continue
                        if fine_cat not in fine_data:
                            fine_data[fine_cat] = [[0.0] * len(iso_codes) for _ in range(len(iso_codes))]
                        fine_data[fine_cat][src_lang_idx][tgt_lang_idx] = dists[cat][fine_cat]

        print("=" * 20)
        print("Averages per group".upper()) 
        for metric in coarse_data:
            print()
            print(metric.upper())
            # TODO rewrite to avoid having pandas as a requirement
            cm_df = pd.DataFrame(coarse_data[metric], index=iso_codes, columns=iso_codes)
            print(cm_df)
        print()
        print("=" * 20) 
        print("Distance scores per feature".upper()) 
        for metric in fine_data:
            print()
            print(metric.upper())
            # TODO rewrite to avoid having pandas as a requirement
            cm_df = pd.DataFrame(fine_data[metric], index=iso_codes, columns=iso_codes)
            print(cm_df)

if __name__ == "__main__":
    main()


