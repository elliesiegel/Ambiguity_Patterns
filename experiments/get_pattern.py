import sys
import json
import os.path
import itertools
import urllib.request

import networkx as nx
import matplotlib.pyplot as plt

'''
collects word information/synsets from BabelNet
creates patterns
'''

# example call: python3 relations.py knot JSON_data/knot_en/

# give the data directory with json files in it
data_dir = sys.argv[2]

# lemma=page --> lemma=word
# first argument "word" 
input_word = sys.argv[1]
print("*"*10)
print("initial word: ", "> ", input_word, " <")
print("*"*10)


def check_files_SynsetIds_exist(data_dir, input_word):
    # if the id file does not exist, create one:
    if os.path.isfile(data_dir + input_word + "_synset_ids.json") == False:

        url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
        url = url.replace("[word]", input_word)
        web_get_synset_ids = urllib.request.urlopen(url)
        data = json.load(web_get_synset_ids) 

        # SAVE data in json if the file with the ids does not exist:
        out_file = open(data_dir + input_word + "_synset_ids.json", "w") 
        json.dump(data, out_file, indent = 6) 
    
        return True
        
def check_files_getSynset_exist(idx):
    if os.path.isfile(data_dir + idx +"_"+ input_word + "_wordsynsets.json") == False:
        # sometimes no senses are given, hence error "IndexError: list index out of range" occurs, so catching
        try:
            # id=bn:00091387v --> id=extracted_id
            url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&targetLang=EN&targetLang=IT&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
            url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
            web_get_synsets = urllib.request.urlopen(url_for_lemmas)
            data_synsets = json.load(web_get_synsets)
            out_file = open(data_dir + idx +"_"+ input_word + "_wordsynsets.json", "w") 
            json.dump(data_synsets, out_file, indent = 6) 
        except:
            pass
        return True
    else:
        return False

def check_files_getSenses_exist(further_word): # for further word
    if os.path.isfile(data_dir + further_word + "_wordSenses.json") == False:
        # CALL if files do not exist else give the files in
        try:
            # [word] may have non ascii chars
            url = "https://babelnet.io/v6/getSenses?lemma=[word]&searchLang=EN&searchLang=DE&searchLang=FR&searchLang=ES&searchLang=IT&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
            url = url.replace("[word]", further_word)
            web_get_synset_ids = urllib.request.urlopen(url)
            further_word_data = json.load(web_get_synset_ids)
            out_file = open(data_dir + further_word + "_wordSenses.json", "w") 
            json.dump(further_word_data, out_file, indent = 6) 
        except:
                pass
        return True
    else: 
        return False

# TODO change to argparse
# TODO: expand / change "searchLang=EN"

files_checker = check_files_SynsetIds_exist(data_dir, input_word)
if files_checker:
    print("files with SynsetIds were created")
else:
    print("files with SynsetIds already exist")
print()

node_lst = []
with open(data_dir + input_word + "_synset_ids.json", "r") as synsets_id_json_file:
    synset_ids = json.load(synsets_id_json_file)
    for elem in synset_ids:
        idx = elem["id"]
        if check_files_getSynset_exist(idx) == False: # the files exist already 
            with open(data_dir + idx +"_"+ input_word + "_wordsynsets.json", "r") as word_synsets_json:
                word_synserts = json.load(word_synsets_json)
                try:
                    node = (word_synserts["senses"][0]["properties"]["fullLemma"], word_synserts["senses"][0]["properties"]["language"])
                    node_lst.append(node)
                except:
                    pass
        else:
            check_files_getSynset_exist(idx)
            ###### copied from above -- TODO node_lst will not be filled with node values
            with open(data_dir + idx +"_"+ input_word + "_wordsynsets.json", "r") as word_synsets_json:
                word_synserts = json.load(word_synsets_json)
                try:
                    node = (word_synserts["senses"][0]["properties"]["fullLemma"], word_synserts["senses"][0]["properties"]["language"])
                    node_lst.append(node)
                except:
                    pass
            ###### 

    print("1st level : ", node_lst)


G = nx.Graph()    

# SAVE further meanings of words in node_lst:
for elem in node_lst:
    G.add_edges_from([(input_word, elem)]) # example elem = ('Page_boy_(wedding_attendant)', 'EN')
    further_word = elem[0]
    if check_files_getSenses_exist(further_word) == False:
        try:
            with open(data_dir + further_word + "_wordSenses.json", "r") as further_word_json:
                further_word_senses = json.load(further_word_json)
                try:
                    further_node = (further_word_senses[0]["properties"]["fullLemma"], further_word_senses[0]["properties"]["language"])
                    print(elem, " --> ", further_node)
                    G.add_edges_from([(elem, further_node)])
                except:
                    pass
        except:
            pass
    else:
        check_files_getSenses_exist(further_word)
        try:
            with open(data_dir + further_word + "_wordSenses.json", "r") as further_word_json:
                further_word_senses = json.load(further_word_json)
                try:
                    further_node = (further_word_senses[0]["properties"]["fullLemma"], further_word_senses[0]["properties"]["language"])
                    print(elem, " --> ", further_node)
                    G.add_edges_from([(elem, further_node)])
                except:
                    pass
        except:
            pass


nx.draw_networkx(G)
plt.show()