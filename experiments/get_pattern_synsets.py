import sys
import glob
import json
# from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt

'''
get number nodes/edges
construct the graph

example call: python3 get_pattern_synsets.py JSON_data/recrimination/
'''

path_to_input_jsons = sys.argv[1]
# path_to_save_word_graph_img = sys.argv[2]
# json_folder = Path(path_to_input_jsons).rglob('*.json')
# files = [f_folder for f_folder in json_folder]

G = nx.Graph()

all_word_nodes = []
wordsynsets = glob.glob(path_to_input_jsons + "*_wordsynsets.json")
wordSenses = glob.glob(path_to_input_jsons + "*_wordSenses.json")


def get_wordsynsets(wordsynsets):
    num_edges_wordsynsets = 0
    num_synset = 0
    # get synsets:
    for synsets_file in wordsynsets:
        node_set = set() # per synset a new one
        num_synset += 1
        # print("synset num: ", num_synset)
        with open(synsets_file) as word_synsets_reader:
            word_synsets = json.load(word_synsets_reader)
            # for synsets from ids - format with senses:
            for one_dict in word_synsets["senses"]:
                # print(one_dict)
                # print()
                try:
                    # if one_dict["properties"]["language"] == "EN" or "DE" or "ES" or "FR":
                    lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                    node_set.add(lemma_and_lang)
                    # G.add_node(lemma_and_lang, role=role)
                except:
                    pass
        # print("----------------------------")
        # print(node_set) # look for further senses of the current sense word - 
                        # find out weather there are connections over ambiguous words to
                        # other synset groups (cliques)

        node_set = list(node_set)   # per synset clique / per file
        # All possible pairs
        for node in node_set:
            all_word_nodes.append(node) # from all documents

        all_synset_nodes = [(a, b) for idx, a in enumerate(node_set) for b in node_set[idx + 1:]]
        G.add_edges_from(all_synset_nodes)
        num_edges_wordsynsets += G.number_of_edges()
    
    return num_edges_wordsynsets


def get_wordSenses(wordSenses):
    num_edges_wordSenses = 0
    node_num_wordSenses = 0
    for sense_file in wordSenses:
        for node in all_word_nodes:
            word = node[0]
            if word in sense_file:
                with open(sense_file) as sense_file_reader:
                    senses = json.load(sense_file_reader)
                    for one_dict in senses:
                        # if one_dict["properties"]["language"] == "EN" or "DE" or "ES" or "FR":
                        lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        node_num_wordSenses += 1
                        # print(word, " --- >> ",lemma_and_lang)
                        G.add_edges_from([(word, lemma_and_lang)])
                        num_edges_wordSenses += 1
    
    return node_num_wordSenses, num_edges_wordSenses


num_edges_wordsynsets = get_wordsynsets(wordsynsets)
node_num_wordSenses, num_edges_wordSenses = get_wordSenses(wordSenses)

total_nodes = len(all_word_nodes) + node_num_wordSenses
# print("len(all_word_nodes): ", len(all_word_nodes))
# print("node_num_wordSenses: ", node_num_wordSenses)
print()
print("total number of nodes:", total_nodes)
print("total number of edges:", num_edges_wordsynsets + num_edges_wordSenses)
# print("number of nodes that can be presented in the graph:", G.number_of_nodes())
# print("number of edges that can be presented in the graph:", G.number_of_edges())


# nx.draw_networkx(G)
# plt.show()
# plt.savefig(path_to_save_word_graph_img)

# monolingual "page": total number of nodes:  32029; total number of edges:  52913