import sys
import glob
import json
import itertools
# from pathlib import Path
import statistics
from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt
from nxviz.plots import CircosPlot

'''
example call: python3 get_sense_graph.py JSON_data_comparison/both_ture/climate/ path_to_img
'''

path_to_input_jsons = sys.argv[1]
path_to_save_img = sys.argv[2]

all_word_nodes = []
wordsynsets = glob.glob(path_to_input_jsons + "*_wordsynsets.json")
# wordSenses = glob.glob(path_to_input_jsons + "*_wordSenses.json")

G = nx.Graph()

def get_wordsynsets(wordsynsets):
    saved_cliques = []
    cnt_clique_words = {}
    num_synset = 0
    num_edges_synsets = 0
    # get synsets:
    for synsets_file in wordsynsets:
        node_set = set() # per synset a new one
        num_synset += 1
        node_set.add(str(num_synset))

        with open(synsets_file) as word_synsets_reader:
            word_synsets = json.load(word_synsets_reader)

            for one_dict in word_synsets["senses"]:
                try:
                    lemma_and_lang = (one_dict["properties"]["fullLemma"] + "_" +one_dict["properties"]["language"])
                    node_set.add(lemma_and_lang)
                    # G.add_node(lemma_and_lang, role=role)
                except:
                    pass
        # print("----------------------------")
        # print(node_set) # look for further senses of the current sense word - 
                        # find out weather there are connections over ambiguous words to
                        # other synset groups (cliques)
        # print("num words in a clique {clique_num} -->".format(clique_num = num_synset), len(node_set))
        cnt_clique_words[num_synset]=len(node_set)
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
    
    cnt_edges_from_clique = []

    all_combis = list(itertools.combinations(saved_cliques, 2))
    for pair in all_combis:
        pair1 = pair[0]
        pair2 = pair[1]
        if pair1 != pair2:
            for word1 in pair1:
                for word2 in pair2:
                    if word1 == word2:
                        # print(word1, word2)
                        # print(pair1, " ---- ", pair2)
                        # print()
                        cnt_edges_from_clique.append(pair1[0])
                        # print("#"*20)
                        G.add_edges_from([(pair1[0], pair2[0])])
                        num_edges_synsets += 1
                        # print(type(pair1[0]), type(pair2[0]))
    cnt_edges_from_a_clique = Counter(cnt_edges_from_clique)

    no_second_degree_edges_nodes = [node for node, degree in dict(G.degree()).items() if degree == 0]
    if len(no_second_degree_edges_nodes) != 0:
        num_synset += 1 # count one node more for init_word_node
        edges_to_init_word_node = 0
        for node in no_second_degree_edges_nodes:
            G.add_edges_from([(node, "init_word_node")])
            edges_to_init_word_node += 1

        num_edges_synsets += edges_to_init_word_node

    return num_synset, num_edges_synsets, cnt_clique_words, cnt_edges_from_a_clique


synsets, synset_edges, cnt_clique_words, cnt_edges_from_a_clique  = get_wordsynsets(wordsynsets)

print("total number cliques: ", synsets)
print("total number clique-edges: ", synset_edges)  # total clique edges from word in cl 1 to word in cl2
# print("number of edges (btw cliques) can be presented in graph: ", G.number_of_edges())

print()
print("number words in a clique --> ", cnt_clique_words)    # number of words in a clique (sub-graph)
print("#"*20)
print("number out clique-edges ->> ", cnt_edges_from_a_clique)  # number of outgoing edges from a clique (sub-graph)

print()
print(" variance btw. words in cliques ", statistics.variance(list(cnt_clique_words.values())))
print(" variance btw. edges out. from cliques ", statistics.variance((list(cnt_edges_from_a_clique.values()))))

c = CircosPlot(graph=G)
c.draw()
# plt.show()
plt.savefig(path_to_save_img)


# pair example:
# (
#     ('26', 'atmosfera_IT', 'clima_ES', 'clima_IT', 'climat_FR', 'climate_EN', 'convention-cadre_FR', 'environnement_FR', 'estado_de_ánimo_ES', 'humeur_FR', 'humor_ES', 'mode_FR', 'mood_EN'), 
#     ('27', "Climat_de_l'Allemagne_FR", 'Deutschlands_Klima_DE', 'German_climate_EN', "Germany's_climate_EN", 'Germany_climate_EN', 'Klima_(Bundesrepublik_Deutschland)_DE', 'Klima_(Deutschland)_DE', 'Klima_(Deutschlands)_DE', 'Klima_Deutschlands_DE', 'Klima_in_Deutschland_DE', 'Klima_in_der_Bundesrepublik_Deutschland_DE', 'Klima_von_Deutschland_DE', 'Klima_von_der_Bundesrepublik_Deutschland_DE', 'climat_(Allemagne)_FR', 'climat_en_Allemagne_FR', 'climate_(Germany)_EN', 'climate_in_Germany_EN', 'climate_of_Germany_EN')
# )