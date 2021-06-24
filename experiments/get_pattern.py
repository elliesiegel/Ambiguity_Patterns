import os
import sys
import json
import os.path
import argparse
import itertools
import urllib.request
import urllib.parse
import pickle
import re
import time
from pathlib import Path
from warnings import catch_warnings


ERROR_BAD_JSON_STRING = "Error: Bad JSON-Formating"

class ApiProxy():

    def __init__(self, dumpfile_path):
        self.dumpfile_path = dumpfile_path
        if os.path.isfile(dumpfile_path):
            raise Exception('dumpfile_path must be a directory!')
        if not os.path.isdir(dumpfile_path):
            os.mkdir(dumpfile_path)

    def _query_until_json(self, url, dump_path):
        while True:
            try:
                web_get_data = urllib.request.urlopen(url)
                json_reply = self._web_get_data_to_json(web_get_data)
                print('Loaded from URL: ', url)
                if 'message' in json_reply:
                    print(json_reply["message"])
                    if ERROR_BAD_JSON_STRING not in json_reply['message']:
                        return json_reply
                with open(dump_path, "w") as out_file:
                    json.dump(json_reply, out_file, indent = 6) 
                return json_reply
            except:
                print("Reqest Faild for: ", url)
                print("Retrying after 5 seconds ...")
                time.sleep(5)

    def _web_get_data_to_json(self, web_get_data):
        try:
            return json.load(web_get_data)
        except:
            return {"message": ERROR_BAD_JSON_STRING}

    def _replace_lang_in_url(self, lang_triplet, url_template):
        lan = lang_triplet.split("_")
        return url_template\
            .replace("[lan_1]", urllib.parse.quote(lan[0]))\
            .replace("[lan_2]", urllib.parse.quote(lan[1]))\
            .replace("[lan_3]", urllib.parse.quote(lan[2]))
    
    def _load_from_dump_file(self, path):
        try:
            print('Loaded Dump-File: ', path)
            with open(path, "r") as f:
                return json.load(f)
        except:
            print('Loading Dump-File failed: ', path)

    # synset_ids
    def make_synset_ids_json_name(self, input_word):
        return input_word + "_synset_ids.json"

    def query_for_synset_ids_json(self, input_word, babel_net_api_key):
        path = self.dumpfile_path + '/' + self.make_synset_ids_json_name(input_word)
        if Path(path).is_file():
            return self._load_from_dump_file(path)
        else:
            url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=[babel_net_api_key]"\
                .replace("[word]", urllib.parse.quote(input_word))\
                .replace("[babel_net_api_key]", urllib.parse.quote(babel_net_api_key))
            return self._query_until_json(url, path)

    # wordsynsets
    def make_wordsynsets_json_name(self, idx, lang_triplet):
        return idx +"_"+ input_word + "_" + lang_triplet + "_wordsynsets.json"

    def query_for_wordsynsets_json(self, idx, lang_triplet, babel_net_api_key):
        path = self.dumpfile_path + '/' + self.make_wordsynsets_json_name(idx, lang_triplet)
        if Path(path).is_file():
            return self._load_from_dump_file(path)
        else:
            url_template = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=[lan_1]&targetLang=[lan_2]&targetLang=[lan_3]&targetLang=EN&key=[babel_net_api_key]"\
                .replace("[synset_id]", urllib.parse.quote(idx))\
                .replace("[babel_net_api_key]", urllib.parse.quote(babel_net_api_key))
            return self._query_until_json(self._replace_lang_in_url(lang_triplet, url_template), path)

    # wordSenses
    def make_wordSenses_json_name(self, further_word, lang_triplet):
        return further_word + "_" + lang_triplet + "_wordSenses.json"

    def query_for_wordSenses_json(self, further_word, lang_triplet, babel_net_api_key):
        path = self.dumpfile_path + '/' + self.make_wordSenses_json_name(idx, targetLang_searchLang)
        if Path(path).is_file():
            return self._load_from_dump_file(path)
        else:
            url_template = "https://babelnet.io/v6/getSenses?lemma=[word]&searchLang=[lan_1]&searchLang=[lan_2]&searchLang=[lan_3]&searchLang=EN&key=[babel_net_api_key]"\
                .replace("[word]", urllib.parse.quote(further_word))\
                .replace("[babel_net_api_key]", urllib.parse.quote(babel_net_api_key))
            return self._query_until_json(self._replace_lang_in_url(lang_triplet, url_template), path)


api_proxy=ApiProxy("DUMP")

# import networkx as nx
# import matplotlib.pyplot as plt

'''
- collects word information/synsets from BabelNet
- optionally: creates patterns (as data is collected)

example call: python3 get_pattern.py recrimination JSON_data/recrimination/
'''

parser = argparse.ArgumentParser()
# Parameters
parser.add_argument(
                    "input_word",
                    default=None,
                    type=str,
                    help="the word we want to get the pattern from."
                    )

parser.add_argument(
                    "data_dir",
                    default=None,
                    type=str,
                    help="Directory where to save documents from the BabelNet API."
                    )

parser.add_argument(
                    "api_key",
                    default="",
                    type=str,
                    help="access api key for babelnet"
                    )

parser.add_argument(
                    "--targetLang_searchLang",  # languages we want to gather information from
                    default="DE_ES_FR",  # "DE_ES_FR", "CS_IT_NN", "RU_UK_PL"
                    type=str,
                    help="languages for search/target (the BabelNet API is restricted to max 3 languages)."
                    )

parser.add_argument(
                    "--languages",  # languages to open files from
                    default="DE_ES_FR",  # "DE_ES_FR", "CS_IT_NN", "RU_UK_PL"
                    type=str,
                    # nargs='+',
                    # default=["DE_ES_FR", "CS_IT_NN", "RU_UK_PL"],
                    help="languages for reading/opening saved BabelNet data."
                    )
# indo-europ.: DE, FR, ES, IT, EN, CS, NN, NO, RU, UK, PL
# others: TR


args = parser.parse_args()

saved_languages = [args.languages]
print(saved_languages, "**********************")

# must be in the saved_languages list
targetLang_searchLang = args.targetLang_searchLang
lang_lst = targetLang_searchLang.split("_")
lan_1 = lang_lst[0]
lan_2 = lang_lst[1]
lan_3 = lang_lst[2]

babel_net_api_key = args.api_key

# give the data directory with json files in it
# data_dir = sys.argv[2]
data_dir = args.data_dir
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# lemma=page --> lemma=word
# first argument "word" 
# input_word = sys.argv[1]
input_word = args.input_word

print("*"*10)
print("initial word: ", "> ", input_word, " <")
print("*"*10)


def creating_files_SynsetIds(data_dir, input_word):
    # if the id file does not exist, create one:
    synset_ids_json_path = data_dir + api_proxy.make_synset_ids_json_name(input_word)
    if not os.path.isfile(synset_ids_json_path):
        # SAVE data in json if the file with the ids does not exist:
        data = api_proxy.query_for_synset_ids_json(input_word, babel_net_api_key)
        with open(synset_ids_json_path, "w") as out_file:
            json.dump(data, out_file, indent = 6)
        return True
    return False
    
        
def download_files_getSynset(idx):
    wordsynsets_json_path = data_dir + api_proxy.make_wordsynsets_json_name(idx, targetLang_searchLang)
    if not os.path.isfile(wordsynsets_json_path):
        # sometimes no senses are given, hence error "IndexError: list index out of range" occurs, so catching
        try:
            data_synsets = api_proxy.query_for_wordsynsets_json(idx, targetLang_searchLang, babel_net_api_key)
            with open(wordsynsets_json_path, "w") as out_file:
                json.dump(data_synsets, out_file, indent = 6) 
        except:
            pass
    return os.path.isfile(wordsynsets_json_path)

def check_files_getSenses_exist(further_word): # for further word
    wordSenses_json_path = data_dir + api_proxy.make_wordSenses_json_name(further_word, targetLang_searchLang)
    if not os.path.isfile(wordSenses_json_path):
        # CALL if files do not exist else give the files in
        try:
            further_word_data = api_proxy.query_for_wordSenses_json(further_word, targetLang_searchLang, babel_net_api_key)
            with open(wordSenses_json_path, "w") as out_file:
                json.dump(further_word_data, out_file, indent = 6) 
        except:
                pass
        return True
    else: 
        return False


if creating_files_SynsetIds(data_dir, input_word):
    print("files with SynsetIds were created")
else:
    print("files with SynsetIds already exist")
print()

node_lst = []
for lang_set in saved_languages:
    with open(data_dir + api_proxy.make_synset_ids_json_name(input_word), "r") as synsets_id_json_file:
        synset_ids = json.load(synsets_id_json_file)
        for elem in synset_ids:
            idx = elem["id"]
            if download_files_getSynset(idx): # the files exist already 
                with open(data_dir + api_proxy.make_wordsynsets_json_name(idx, targetLang_searchLang), "r") as word_synsets_json:
                    word_synserts = json.load(word_synsets_json)
                    try:
                        for one_dict in word_synserts:
                            # print(one_dict["properties"])
                            # print()
                            lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                            node_lst.append(lemma_and_lang)
                            # print("**********************************************")
                    except:
                        for one_dict in word_synserts["senses"]:
                            # print(one_dict["properties"])
                            # print()
                            lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                            node_lst.append(lemma_and_lang)
                            # print("**********************************************")
  

    print("1st level : ", node_lst)
    node_num1 = len(node_lst)
    print("number of nodes 1st level : ", node_num1)


# G = nx.Graph()

# num_edges = 0
# SAVE further meanings of words in node_lst:
for elem in node_lst:
    # G.add_edges_from([(input_word, elem)]) # example elem = ('Page_boy_(wedding_attendant)', 'EN')
    # num_edges += 1
    further_word = elem[0]
    if not check_files_getSenses_exist(further_word):
        for lang_set in saved_languages:
            try:
                with open(data_dir + api_proxy.make_wordSenses_json_name(further_word, lang_set), "r") as further_word_json:
                    further_word_senses = json.load(further_word_json)
                    for one_dict in further_word_senses:
                        node_num1 += 1
                        further_node = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        # print(elem, " --> ", further_node)
                        # G.add_edges_from([(elem, further_node)])
                        # num_edges += 1
            except:
                pass

# print()
# print("Final numbers:")
# print("number nodes: ", node_num1)
# print("number edges: ", num_edges)

# nx.draw_networkx(G)
# plt.show()
