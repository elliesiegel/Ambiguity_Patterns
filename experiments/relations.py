import sys
import json
import itertools
import urllib.request

import networkx as nx
import matplotlib.pyplot as plt


# give the data directory with json files in it
data_dir = sys.argv[2]

# lemma=page --> lemma=word
# first argument "word" 
input_word = sys.argv[1]
print("*"*10)
print("initial word: ", "> ", input_word, " <")
print("*"*10)
# TODO: expand / change "searchLang=EN"
# Comment out if limt reached ; if file with the word exists, skip:
# url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
# url = url.replace("[word]", input_word)
# web_get_synset_ids = urllib.request.urlopen(url)
# data = json.load(web_get_synset_ids) 

# SAVE data in json if the file with the ids does not exist:
# out_file = open(input_word + "_synset_ids.json", "w") 
# json.dump(data, out_file, indent = 6) 


# LOADING json
node_lst = []
with open(data_dir + "synset_page_ids.json", "r") as synsets_id_json_file:
    synset_ids = json.load(synsets_id_json_file)
    for elem in synset_ids:
        idx = elem["id"]
#         # sometimes no senses is given, hence error "IndexError: list index out of range" occurs, so catching
#         try:
#             # id=bn:00091387v --> id=extracted_id
#             url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&targetLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
#             url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
#             web_get_synsets = urllib.request.urlopen(url_for_lemmas)
#             data_synsets = json.load(web_get_synsets) 
#             out_file = open(idx +"_"+ input_word + "_wordsynsets.json", "w") 
#             json.dump(data_synsets, out_file, indent = 6) 
#         except:
#             pass

        with open(data_dir + idx +"_"+ input_word + "_wordsynsets.json", "r") as word_synsets_json:
            word_synserts = json.load(word_synsets_json)
            node = (word_synserts["senses"][0]["properties"]["fullLemma"], word_synserts["senses"][0]["properties"]["language"])
            node_lst.append(node)

print("1st level : ", node_lst)

# for idx in word_syns_ids:
#     # sometimes no senses is given, hence error "IndexError: list index out of range" occurs, so catching
#     try:
#         # id=bn:00091387v --> id=extracted_id from word_syns_ids
#         url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&targetLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
#         url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
#         web_get_synsets = urllib.request.urlopen(url_for_lemmas)
#         # web_get_synsets = requests.get(url_for_lemmas)
#         # print(web_get_synsets)
#         data_synsets = json.load(web_get_synsets) 
#         node = (data_synsets["senses"][0]["properties"]["fullLemma"], data_synsets["senses"][0]["properties"]["language"])
#         node_lst.append(node)
#     except:
#         pass


G = nx.Graph()    

# SAVE further meanings of words in node_lst:
for elem in node_lst:
    G.add_edges_from([(input_word, elem)]) # example elem = ('Page_boy_(wedding_attendant)', 'EN')
    further_word = elem[0]

    # COMMENT OUT if files do not exist else give the files in
    # try:
    #     # [word] may have non ascii chars
    #     url = "https://babelnet.io/v6/getSenses?lemma=[word]&searchLang=EN&searchLang=DE&searchLang=FR&searchLang=ES&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
    #     url = url.replace("[word]", further_word)
    #     web_get_synset_ids = urllib.request.urlopen(url)
    #     further_word_data = json.load(web_get_synset_ids)
    #     out_file = open(further_word + "_wordSenses.json", "w") 
    #     json.dump(further_word_data, out_file, indent = 6) 
    # except:
    #     pass

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