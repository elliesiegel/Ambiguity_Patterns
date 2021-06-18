import csv
from os import read
import sys

'''
example call: 
python3 to_buckets.py RESULTS_figure_CSV/all-trues-word-nodes-edges.csv
python3 to_buckets.py RESULTS_figure_CSV/all-falses-word-nodes-edges.csv
'''

input_csv = sys.argv[1]
bucket_1 = []
bucket_2 = []
bucket_3 = []

clique_num_bucket_1 = []
clique_num_bucket_2 = []
clique_num_bucket_3 = []

with open(input_csv, "r") as reader_csv:
    reader = csv.reader(reader_csv)
    for row in reader:
        word = row[0]
        
        nodes = int(row[1])
        edges = int(row[2])

        cliques = int(row[3])
        clique_edges = int(row[4])

        if nodes < 100000 and edges < 100000:
            bucket_1.append((word, nodes, edges))
        
        if 100000 < nodes < 1000000 and 100000 < edges < 1000000:
            bucket_2.append((word, nodes, edges))

        if 1000000 < nodes and 1000000 < edges:
            bucket_3.append((word, nodes, edges))


        if cliques < 10 and clique_edges < 200:
            clique_num_bucket_1.append((word, cliques, clique_edges))
        
        if 10 < cliques < 100 and 200 < clique_edges < 1000:
            clique_num_bucket_2.append((word, cliques, clique_edges))

        if 100 < cliques and 1000 < clique_edges:
            clique_num_bucket_3.append((word, cliques, clique_edges))


# print(bucket_1)
# print("#"*20)
# print(bucket_2)
# print("#"*20)
# print(bucket_3)

print()
print("bucket 1: ", clique_num_bucket_1)
print("#"*20)
print()
print("bucket 2: ", clique_num_bucket_2)
print("#"*20)
print()
print("bucket 3: ", clique_num_bucket_3)
print()

# bucket_2 ###########
# only over nodes
# ('temperature', 678597, true) - ('Appeal', 674733, false)
# Appeal:   variance btw. words in cliques 962.4272727272726
#           variance btw. edges out. from cliques  4108.0609756097565
# temperature:  variance btw. words in cliques 1286.076923076923
#               variance btw. edges out. from cliques  3769.528571428572


# nodes and edges:
# ('advantage', 419214, 479607, false) - ('bacteria', 405885, 525620, true)
# diff: 13329 nodes / 46013 edges

# ('breach', 745428, 977668, false) - ('temperature', 678597, 920461, tures)
# diff: 66831 nodes / 57207 edges

# ('company', 233195, 360786, false) - ('advice', 211758, 249925, true)
# diff: 21437 nodes / 110861 edges

# ('concentration', 707939, 859144, false) - ('temperature', 678597, 920461, true)
# diff: 29342 nodes / 61317 edges

###########

# bucket_3 ###########
# nodes and edges:
# ('barrel', 2257731, 2683108, false) - ('chairman', 2317884, 2945698, true)
# diff: 60153 edges / 262590

# ('barrel', 2257731, 2683108, false) - ('century', 2033823, 2885156, true)
# diff: 223908 nodes / 202048 edges

# ('boost', 1731915, 2869820, false) - ('adaptation', 1711497, 2053998, true)
# diff: 20418 nodes / 815822 edges

########## ('chart', 2030871, 2364886, false) - ('CEO', 2042724, 2318986, true)  ##########
# diff: 11853 nodes / 45900 edges
# CEO: cliques 21 / clique edges 900
# chart: cliques 30 / clique edges 1332
 
# ('closing', 1907454, 2152133, false) - ('adaptation', 1711497, 2053998, true)
# diff: 195957 nodes / 98135 edges

##############################################################################################

# over cliques and clique edges, true/true vs false/false:

# ('barrel', 33, 2196, false) - ('chairman', 33, 1422, true)
# ('closing', 36, 1752, false) - ('adaptation', 33, 1878, true)

# ('advantage', 30, 852, false) - ('applause', 27, 957, true)
# ('challenge', 138, 6531, false) - ('attitude', 108, 6792, true)

# ('Central_America', 12, 543, false) - ('biochemistry', 12, 585, true)
# ('Code_of_Conduct', 12, 426, false) - ('biochemistry', 12, 585, true)
# ('fault_lines', 12, 243, false) - ('biochemistry', 12, 585, true)
# ('fault_lines', 12, 243, false) - ('backing', 15, 282, true)

# ('circumstances', 18, 579, false) - ('bacteria', 18, 864, true)
# ('circumstances', 18, 579, false) - ('arsenic', 18, 912, true)
# ('advantage', 30, 852, false) - ('applause', 27, 957, true)
# ('fault_lines', 12, 243, false) - ('competitor', 15, 228, true)
# ('club', 117, 10215, false) - ('attitude', 108, 6792, true)

### the variance with weights (clique words + clique edges) is highes with True/True and lower with False/False


# true / false vs false / true accord. to cliques and clique-edges

# ('posturing', 3, 3, true_false) - ('reductions', 3, 24, false_true)
# ('announcement', 18, 615, true_false) - ('capability', 18, 768, false_true)
# ('basis', 48, 697, true_false) - ('bonus', 42, 798, false_true)
# ('conference', 30, 544, true_false) - ('questions', 30, 524, false_true)