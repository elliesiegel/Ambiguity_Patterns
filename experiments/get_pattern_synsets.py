import sys
import json
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


path_to_input_jsons = sys.argv[1]
json_folder = Path(path_to_input_jsons).rglob('*.json')
files = [f_folder for f_folder in json_folder]


G = nx.Graph()

# get synsets
num_synset = 0
for one_f in files: # one_f == one synset for a given word
    node_set = set() # per synset a new one
    num_synset += 1
    role = "synset_"+ str(num_synset)
    with open(one_f) as word_synsets_reader:
        word_synsets = json.load(word_synsets_reader)
        # for synsets from ids - format with senses:
        for one_dict in word_synsets["senses"]:
            # print(one_dict)
            # print()
            try:
                if one_dict["properties"]["language"] == "EN" or "DE" or "ES":
                    lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
                    node_set.add(lemma_and_lang)
                    # G.add_node(lemma_and_lang, role=role)
            except:
                pass
    # print("----------------------------")
    # print(node_set) # look for further senses of the current sense word - 
                    # find out weather there are connections over ambiguous words to
                    # other synset groups (cliques)

    node_set = list(node_set)
    # All possible pairs
    all_synset_nodes = [(a, b) for idx, a in enumerate(node_set) for b in node_set[idx + 1:]]
    # print(all_synset_nodes)
    G.add_edges_from(all_synset_nodes)

nx.draw_networkx(G)
plt.show()

# num files:    
# print(len(files))