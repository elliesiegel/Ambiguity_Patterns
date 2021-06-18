import re
import sys
import numpy as np


# python3 calc_avg_variance.py vars_results/vars_weight_clique_edges/4_var_edges_cliques_true_false.txt

# to get variance number data: 
# cat 4_var_true_false.txt | grep " variance btw. edges out. from cliques  " > vars_weight_clique_edges/4_var_edges_cliques_true_false.txt
# cat 1_var_both_true.txt | grep "variance btw. words in cliques"  > vars_weights_clique_nodes/1_var_words_in_cliques_both_true.txt


input_numbers_file = sys.argv[1]

def get_avg_var(in_file):
    var_lst = []
    with open(in_file) as input_file:
        reader = input_file.readlines()

    for line in reader:

        var_num = re.sub("\n", "", line)
        var_num = re.sub(" ", "", var_num)
        var_num = float(var_num)
        var_lst.append(var_num)

    return var_lst


variance_list = get_avg_var(input_numbers_file)
var_avg = np.average(variance_list)

print(var_avg)

# (word within cliques) avg variance of
# true / true: 1342.2819911924914
# false / true: 624.6766128906326   (min)
# true / false: 1579.6725494578716  (max)
# false / false: 1477.6311723783444

# (edges of cliques weights) avg variance of
# true / true: 5659.284257238339
# false / true: 2818.925610210361   (min)
# true / false: 5963.547082666545   (max)
# false / false: 5026.296314015574