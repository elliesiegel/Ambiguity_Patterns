import sys
import glob
import json
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


path_to_input_jsons = sys.argv[1]
# json_folder = Path(path_to_input_jsons).rglob('*.json')
# files = [f_folder for f_folder in json_folder]

G = nx.Graph()

all_word_nodes = []
wordsynsets = glob.glob(path_to_input_jsons + "*_wordsynsets.json")
wordSenses = glob.glob(path_to_input_jsons + "*_wordSenses.json")


def get_wordsynsets(wordsynsets):
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
                    if one_dict["properties"]["language"] == "EN":# or "DE" or "ES":
                        lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                        node_set.add(lemma_and_lang)
                        # G.add_node(lemma_and_lang, role=role)
                except:
                    pass
        # print("----------------------------")
        # print(node_set) # look for further senses of the current sense word - 
                        # find out weather there are connections over ambiguous words to
                        # other synset groups (cliques)

        node_set = list(node_set)   # per synset clique
        # All possible pairs
        for node in node_set:
            all_word_nodes.append(node)

        all_synset_nodes = [(a, b) for idx, a in enumerate(node_set) for b in node_set[idx + 1:]]
        G.add_edges_from(all_synset_nodes)


def get_wordSenses(wordSenses):
    for sense_file in wordSenses:
        for node in all_word_nodes:
            word = node[0]
            if word in sense_file:
                with open(sense_file) as sense_file_reader:
                    senses = json.load(sense_file_reader)
                    for one_dict in senses:
                        if one_dict["properties"]["language"] == "EN":# or "DE" or "ES":
                            lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                            # print(word, " --- >> ",lemma_and_lang)
                            G.add_edges_from([(word, lemma_and_lang)])


get_wordsynsets(wordsynsets)
get_wordSenses(wordSenses)

nx.draw_networkx(G)
plt.show()
