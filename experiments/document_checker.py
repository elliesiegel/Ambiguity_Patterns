import itertools
import filecmp
import glob
import sys
import os


# path_to_input_jsons = sys.argv[1]
# wordSenses = glob.glob(path_to_input_jsons + "*_wordSenses.json")
# print(len(wordSenses))


def check_docs_not_same(files_directory):
    wordSenses = glob.glob(files_directory + "*_wordSenses.json")

    # simulating permutations of the list in a group of 2
    pair_order_list = itertools.permutations(wordSenses, 2)
    
    # printing the elements belonging to permutations
    all_combs = list(pair_order_list)
    
    for comb_tuple in all_combs:
        file1 = comb_tuple[0]
        file2 = comb_tuple[1]

        if file2 != file1:
            try:
                true_false = filecmp.cmp(file1, file2)

                if true_false == True:
                    print(file1, " ####### ",file2)
                    os.remove(file2)
            except:
                pass

def check_docs_not_empty(files_directory):
    wordSenses = glob.glob(files_directory + "*_wordSenses.json")

    for f in wordSenses:
        with open(f) as document:
            document_first_line = document.readline()
            if document_first_line == "[]":
                # print(f, " - empty doc")
                os.remove(f)


files_directory = sys.argv[1]
check_docs_not_same(files_directory)
# check_docs_not_empty(files_directory)
