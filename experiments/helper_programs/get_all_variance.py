import os
import sys

# example call: python3 get_all_variance.py JSON_data_comparison_2/both_false/words/

input_dir_path = sys.argv[1]
lst_dir_names = os.listdir(input_dir_path)


for word in lst_dir_names:
    os.system("python3 get_sense_graph.py " + input_dir_path + word + "/" + " .")
    #print("python3 get_sense_graph.py " + input_dir_path + word + "/" + " .")
