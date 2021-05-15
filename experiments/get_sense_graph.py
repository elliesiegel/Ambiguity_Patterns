import sys
import glob
import json
import itertools
# from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
from nxviz.plots import CircosPlot

'''
example call: python3 get_sense_graph.py JSON_data_comparison/both_ture/climate/
'''

path_to_input_jsons = sys.argv[1]

all_word_nodes = []
wordsynsets = glob.glob(path_to_input_jsons + "*_wordsynsets.json")
# wordSenses = glob.glob(path_to_input_jsons + "*_wordSenses.json")

G = nx.Graph()

def get_wordsynsets(wordsynsets):
    saved_cliques = []
    num_synset = 0
    # get synsets:
    for synsets_file in wordsynsets:
        node_set = set() # per synset a new one
        num_synset += 1
        node_set.add(str(num_synset))

        with open(synsets_file) as word_synsets_reader:
            word_synsets = json.load(word_synsets_reader)

            for one_dict in word_synsets["senses"]:
                try:
                    if one_dict["properties"]["language"] == "EN" or "DE" or "ES" or "FR":
                        # lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        lemma_and_lang = (one_dict["properties"]["fullLemma"] + "_" +one_dict["properties"]["language"])
                        node_set.add(lemma_and_lang)
                        # G.add_node(lemma_and_lang, role=role)
                except:
                    pass
        # print("----------------------------")
        # print(node_set) # look for further senses of the current sense word - 
                        # find out weather there are connections over ambiguous words to
                        # other synset groups (cliques)
        node_set = sorted(node_set)
        node_lst = tuple(node_set)   # per synset clique / per file

        saved_cliques.append(node_lst)
        G.add_node(str(num_synset))
        # All possible pairs
        # for node in node_lst:
        #     all_word_nodes.append(node) # from all documents

        # all_synset_nodes = [(a, b) for idx, a in enumerate(node_set) for b in node_set[idx + 1:]]
        # G.add_edges_from(all_synset_nodes)
        # num_edges_wordsynsets += G.number_of_edges()
    
    all_combis = list(itertools.combinations(saved_cliques, 2))
    for elem in all_combis:
        elem1 = elem[0]
        elem2 = elem[1]
        if elem1 != elem2:
            for word1 in elem1:
                for word2 in elem2:
                    if word1 == word2:
                        # print(word1, word2)
                        # print(elem1[0], " ---- ", elem2[0])
                        G.add_edges_from([(elem1[0], elem2[0])])
                        # print(type(elem1[0]), type(elem2[0]))
    
    return num_synset


synsets = get_wordsynsets(wordsynsets)
print("total number cliques: ", synsets)

c = CircosPlot(graph=G)
c.draw()
plt.show()
