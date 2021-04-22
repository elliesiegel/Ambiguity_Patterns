import os
import sys
import json
import os.path
import argparse
import itertools
import urllib.request

import networkx as nx
import matplotlib.pyplot as plt

'''
- collects word information/synsets from BabelNet
- creates patterns

example call: python3 get_pattern.py knot JSON_data/knot_en/
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
                    "--targetLang_searchLang",  # languages we want to gather information from
                    default="DE_ES_FR", # CS_IT_NN   RU_UK_PL
                    type=str,
                    help="languages for search/target (the BabelNet API is restricted to max 3 languages)."
                    )

parser.add_argument(
                    "--languages",  # languages to open files from
                    nargs='+',
                    default=["DE_ES_FR", "CS_IT_NN", "RU_UK_PL"],
                    help="languages for reading/opening saved BabelNet data."
                    )
# indo-europ.: DE, FR, ES, IT, EN, CS, NN, NO, RU, UK, PL
# others: TR

args = parser.parse_args()

saved_languages = args.languages
print(saved_languages, "**********************")

# must be in the saved_languages list
targetLang_searchLang = args.targetLang_searchLang
lang_lst = targetLang_searchLang.split("_")
lan_1 = lang_lst[0]
lan_2 = lang_lst[1]
lan_3 = lang_lst[2]

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


# TODO: expand / change "searchLang=EN" to argparse arg
def check_files_SynsetIds_exist(data_dir, input_word):
    # if the id file does not exist, create one:
    if os.path.isfile(data_dir + input_word + "_" + targetLang_searchLang + "_synset_ids.json") == False:

        url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
        url = url.replace("[word]", input_word)
        web_get_synset_ids = urllib.request.urlopen(url)
        data = json.load(web_get_synset_ids) 

        # SAVE data in json if the file with the ids does not exist:
        out_file = open(data_dir + input_word + "_" + targetLang_searchLang + "_synset_ids.json", "w") 
        json.dump(data, out_file, indent = 6) 
    
        return True
        
def check_files_getSynset_exist(idx, lan_1, lan_2, lan_3):
    if os.path.isfile(data_dir + idx +"_"+ input_word + "_" + targetLang_searchLang + "_wordsynsets.json") == False:
        # sometimes no senses are given, hence error "IndexError: list index out of range" occurs, so catching
        try:
            # id=bn:00091387v --> id=extracted_id
            url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=[lan_1]&targetLang=[lan_2]&targetLang=[lan_3]&targetLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
            url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
            url_for_lemmas = url_for_lemmas.replace("[lan_1]", lan_1)
            url_for_lemmas = url_for_lemmas.replace("[lan_2]", lan_2)
            url_for_lemmas = url_for_lemmas.replace("[lan_3]", lan_3)

            web_get_synsets = urllib.request.urlopen(url_for_lemmas)
            data_synsets = json.load(web_get_synsets)
            out_file = open(data_dir + idx +"_"+ input_word + "_" + targetLang_searchLang + "_wordsynsets.json", "w") 
            json.dump(data_synsets, out_file, indent = 6) 
        except:
            pass
        return True
    else:
        return False

def check_files_getSenses_exist(further_word, lan_1, lan_2, lan_3): # for further word
    if os.path.isfile(data_dir + further_word + "_" + targetLang_searchLang + "_wordSenses.json") == False:
        # CALL if files do not exist else give the files in
        try:
            # [word] may have non ascii chars
            url = "https://babelnet.io/v6/getSenses?lemma=[word]&searchLang=[lan_1]&searchLang=[lan_2]&searchLang=[lan_3]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
            url = url.replace("[word]", further_word)
            url = url.replace("[lan_1]", lan_1)
            url = url.replace("[lan_2]", lan_2)
            url = url.replace("[lan_3]", lan_3)

            web_get_synset_ids = urllib.request.urlopen(url)
            further_word_data = json.load(web_get_synset_ids)
            out_file = open(data_dir + further_word + "_" + targetLang_searchLang + "_wordSenses.json", "w") 
            json.dump(further_word_data, out_file, indent = 6) 
        except:
                pass
        return True
    else: 
        return False


files_checker = check_files_SynsetIds_exist(data_dir, input_word)
if files_checker:
    print("files with SynsetIds were created")
else:
    print("files with SynsetIds already exist")
print()

node_lst = []
for lang_set in saved_languages:
    with open(data_dir + input_word + "_" + lang_set + "_synset_ids.json", "r") as synsets_id_json_file:
        synset_ids = json.load(synsets_id_json_file)
        for elem in synset_ids:
            idx = elem["id"]
            if check_files_getSynset_exist(idx, lan_1, lan_2, lan_3) == False: # the files exist already 
                with open(data_dir + idx +"_"+ input_word + "_" + lang_set + "_wordsynsets.json", "r") as word_synsets_json:
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
            else:
                check_files_getSynset_exist(idx, lan_1, lan_2, lan_3)
                ###### copied from above -- TODO node_lst will not be filled with node values
                with open(data_dir + idx +"_"+ input_word + "_" + lang_set + "_wordsynsets.json", "r") as word_synsets_json:
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
                ###### 

    print("1st level : ", node_lst)


G = nx.Graph()

# SAVE further meanings of words in node_lst:
for elem in node_lst:
    G.add_edges_from([(input_word, elem)]) # example elem = ('Page_boy_(wedding_attendant)', 'EN')
    further_word = elem[0]
    if check_files_getSenses_exist(further_word, lan_1, lan_2, lan_3) == False:
        for lang_set in saved_languages:
            try:
                with open(data_dir + further_word + "_" + lang_set + "_wordSenses.json", "r") as further_word_json:
                    further_word_senses = json.load(further_word_json)
                    for one_dict in further_word_senses:
                        further_node = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        print(elem, " --> ", further_node)
                        G.add_edges_from([(elem, further_node)])
            except:
                pass
    else:
        check_files_getSenses_exist(further_word, lan_1, lan_2, lan_3)
        for lang_set in saved_languages:
            try:
                with open(data_dir + further_word + "_" + lang_set + "_wordSenses.json", "r") as further_word_json:
                    further_word_senses = json.load(further_word_json)
                    for one_dict in further_word_senses:
                        further_node = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        print(elem, " --> ", further_node)
                        G.add_edges_from([(elem, further_node)])
            except:
                pass


# nx.draw_networkx(G)
# plt.show()

from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx

# G = nx.karate_club_graph()

plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
              tools="", toolbar_location=None)

graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0)) # Error !!!
# raise ValueError(f"failed to validate {obj_repr}.{name}: {error}")
# ValueError: failed to validate StaticLayoutProvider(id='1031', ...).graph_layout: 
# expected an element of Dict(Either(String, Int), Seq(Any)), got {'wrestling': array([-0.262687  ,  0.20170794])

plot.renderers.append(graph)

output_file("networkx_graph.html")
show(plot)