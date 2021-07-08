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

# clique / clique-edges for TT vs. FF:

# ('auctions', 3, 92, false) - ('banalities', 3, 84, true)
# 1012.3333333333333,200     -   0,392

# ('New_York_Stock_Exchange', 4, 94, false) - ('banalities', 3, 84, true)
# 290.3333333333333,968                     - 0,392

# ('life_forms', 3, 24, false) - ('investors', 3, 21, true)
# 1.3333333333333333,32        - 74.33333333333333,24.5

# ('life_forms', 3, 24, false) - ('reductions', 3, 24, true)
# 1.3333333333333333,32        - 133.33333333333334,32

# ('Freddie_Mac', 3, 36, false) - ('cameras', 3, 42, true)
# 175,162                       - 161.33333333333331,98

# ('obligations', 3, 30, false) - ('cameras', 3, 42, true)
# 114.33333333333333,50         - 161.33333333333331,98

# ('obligations', 3, 30, false) - ('culpability', 3, 31, true)
# 114.33333333333333,50         - 154.33333333333331,40.5

# ('obligations', 3, 30, false) - ('hordes', 3, 24, true)
# 114.33333333333333,50         - 0.3333333333333333,32

# ('Freddie_Mac', 3, 36, false) - ('culpability', 3, 31, true)
# 175,162                       - 154.33333333333331,40.5

# ('courts', 9, 84, false) - ('imposition', 9, 78, true)
# ('National_Institutes_of_Health', 6, 114, false) - ('risks', 6, 139, true)
# ('courts', 9, 84, false) - ('reporting', 9, 88, true)
# ('justices', 3, 101, false) - ('waiters', 3, 105, true)
# (life_forms', 3, 24, false) - ('economists', 3, 25, true)
# ('narrow_margin', 9, 49, false) - ('responsiveness', 9, 49, true)
# ('narrow_margin', 9, 49, false) - ('ruling', 9, 50, true)
# ('auctions', 3, 92, false) - ('prosecutors', 3, 95, true)


# ('acceptance', 45, 659, false) - ('election', 42, 679, true)
# ('photographs', 27, 366, false) - ('proposal', 27, 356, true)
# ('publication', 15, 320, false) - ('immigrants', 15, 303, true)
# ('publication', 15, 320, false) - ('Immigration', 15, 313, true)
# ('hard_time', 24, 309, false) - ('poverty', 24, 303, true)
# ('robustness', 24, 345, false) - ('poverty', 24, 303, true)
# ('growth', 39, 712, false) - ('height', 39, 754, true)
# ('violence', 45, 630, false) - ('matter', 48, 580, true)
# ('things', 33, 546, false) - ('lawyer', 33, 517, true)
# ('Department_of_Energy', 27, 410, false) - ('imperative', 27, 359, true)
# ('speculation', 21, 387, false) - ('heading', 21, 340, true)
# ('things', 33, 546, false) - ('intention', 33, 487, true)
# ('appearance', 30, 507, false) - ('verdict', 30, 526, true)
# ('appearance', 30, 507, false) - ('ethos', 31, 512, true)
# ('spite', 24, 212, false) - ('Nicaragua', 22, 243, true)


# ('advance', 144, 7176, false) - ('discovery', 157, 8073, true)
# ('tone', 118, 4213, false) - ('firm', 120, 5150, true)
#  - ('law', 132, 3789, true)



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

### the variance with weights (clique words + clique edges) is higher with True/True and lower with False/False


# true / false vs false / true accord. to cliques and clique-edges

# ('posturing', 3, 3, true_false) - ('reductions', 3, 24, false_true)
# ('announcement', 18, 615, true_false) - ('capability', 18, 768, false_true)
# ('basis', 48, 697, true_false) - ('bonus', 42, 798, false_true)
# ('conference', 30, 544, true_false) - ('questions', 30, 524, false_true)