import json
import urllib.request
import sys
import networkx as nx
import matplotlib.pyplot as plt
import itertools

# lemma=page --> lemma=word
# first argument "word" 
input_word = sys.argv[1]
print("*"*10)
print("initial word: ", "> ", input_word, " <")
print("*"*10)

# TODO: expand / change "searchLang=EN"
# Comment out if limt reached:
url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
url = url.replace("[word]", input_word)
web_get_synset_ids = urllib.request.urlopen(url)
data = json.load(web_get_synset_ids) 

# print(data)
# print(type(data))

# elem = id, pos, source
word_syns_ids = []
for elem in data:
    word_syns_ids.append(elem["id"]) # type dict

# idx = word_syns_ids[0]
# print(idx)
# url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
# url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
# web_get_synsets = urllib.request.urlopen(url_for_lemmas)
# print(web_get_synsets)

# import requests
# headers = {
#  'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
# }
node_lst = []
for idx in word_syns_ids:
    # sometimes no senses is given, hence error "IndexError: list index out of range" occurs, so catching
    try:
        # id=bn:00091387v --> id=extracted_id from word_syns_ids
        url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&targetLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
        url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
        web_get_synsets = urllib.request.urlopen(url_for_lemmas)
        # web_get_synsets = requests.get(url_for_lemmas)
        # print(web_get_synsets)
        data_synsets = json.load(web_get_synsets) 
        node = (data_synsets["senses"][0]["properties"]["fullLemma"], data_synsets["senses"][0]["properties"]["language"])
        node_lst.append(node)
    except:
        pass


G = nx.Graph()    
##############################
# G.add_nodes_from(node_lst)

# language_node_lst_EN = []
# language_node_lst_DE = []
# language_node_lst_ES = []
# language_node_lst_FR = []

# for node in node_lst:
#     language = node[1]
#     if language == 'EN':
#         language_node_lst_EN.append(node)
#     if language == 'DE':
#         language_node_lst_DE.append(node)
#     if language == 'ES':
#         language_node_lst_ES.append(node)
#     if language == 'FR':
#         language_node_lst_FR.append(node)

# G.add_nodes_from(language_node_lst_EN)
# for elem in language_node_lst_EN:
#     G.add_edges_from([(input_word, elem)])
##############################


for elem in node_lst:
    G.add_edges_from([(input_word, elem)])
    further_word = elem[0]                      # TODO
    url = "https://babelnet.io/v6/getSenses?lemma=bank&searchLang=EN&searchLang=DE&searchLang=FR&searchLang=ES&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
    url = url.replace("[word]", further_word)
    web_get_synset_ids = urllib.request.urlopen(url)
    further_word_data = json.load(web_get_synset_ids)
    # print("-"*20)
    # # print(further_word_data)
    # next_sense_node = (further_word_data[0]["properties"]) #[0]["fullLemma"], further_word_data["properties"]["language"])
    # print("next: ", next_sense_node)
    # G.add_edges_from([(elem, next_elem_sense)])



# print(language_node_lst_EN)
# print()
# combine_pairs = [(node1, node2) for node1 in test_tuple1 for node2 in test_tuple2]
# combis_within_lan = list(itertools.combinations(language_node_lst_EN, 2)) # list of 2 tuples in a tuple: [( (),() )]

# for elem in combis_within_lan:
#     G.add_edges_from([elem])

# nx.draw_networkx(G)
# plt.show()