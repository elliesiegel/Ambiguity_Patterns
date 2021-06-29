import pandas
import math
import sys


# python3 get_average.py JSON_data_comparison_2/both_false/RESULTS_figure_CSV/word-nodes-edges.csv


input_file = sys.argv[1]
colnames = ['word', 'nodes', 'edges', 'num_cliques', 'num_clique_edges', 'var_words_cliques', 'var_edges_cliques']
data = pandas.read_csv(input_file, names=colnames)

nodes_lst = data.nodes.tolist()
print("nodes avg.: ", sum(nodes_lst) / len(nodes_lst))

edges_lst = data.edges.tolist()
print("edges avg.:", sum(edges_lst) / len(edges_lst))

num_cliques_lst = data.num_cliques.tolist()
print("num cliques avg.:", sum(num_cliques_lst) / len(num_cliques_lst))

num_clique_edges_lst = data.num_clique_edges.tolist()
print("num clique edges avg.:", sum(num_clique_edges_lst) / len(num_clique_edges_lst))

var_words_cliques_lst = data.var_words_cliques.tolist()
var_words_cliques_lst_clean = [num for num in var_words_cliques_lst if math.isnan(num) == False]
print("variance words cliques avg.:", sum(var_words_cliques_lst_clean) / len(var_words_cliques_lst_clean))

var_edges_cliques_lst = data.var_edges_cliques.tolist()
var_edges_cliques_lst_clean = [num for num in var_edges_cliques_lst if math.isnan(num) == False]
print("variance edges cliques avg.:", sum(var_edges_cliques_lst_clean) / len(var_edges_cliques_lst_clean))

#################################################
# all trues filtered:
# nodes avg.: 4480948.864864865
# edges avg.: 5310462.918918919
# num cliques avg.: 41.270270270270274
# num clique edges avg.: 2507.027027027027

# all falses filtered:
# nodes avg.:  6568976.0322580645
# edges avg.: 7978589.161290322
# num cliques avg.: 55.45161290322581
# num clique edges avg.: 3363.967741935484
#################################################

# all trues not filtered:
# nodes avg.:  3955624.285714286
# edges avg.: 4691148.071428572
# num cliques avg.: 37.0
# num clique edges avg.: 2247.0714285714284

# all falses not filtered:
# nodes avg.:  4717738.431818182
# edges avg.: 5742004.7272727275
# num cliques avg.: 44.52272727272727
# num clique edges avg.: 2700.068181818182
#################################################