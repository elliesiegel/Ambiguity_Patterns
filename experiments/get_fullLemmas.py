import sys
import re
import json


node_lst = []
# with open(sys.argv[1], "r") as word_synsets_json:
#     word_synsets = word_synsets_json.read()

# print(word_synsets)
    
    # try:
    #     node = (word_synserts["senses"][0]["properties"]["fullLemma"], word_synserts["senses"][0]["properties"]["language"])
    #     node_lst.append(node)
    # except:
    #     pass

with open(sys.argv[1], "r") as word_synsets_json:
    word_synserts = json.load(word_synsets_json)
    try:
        for one_dict in word_synserts:
            print(one_dict["properties"])
            # print()
            lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
            node_lst.append(lemma_and_lang)
            # print("**********************************************")
    except:
        for one_dict in word_synserts["senses"]:
            # print(one_dict["properties"])
            # print()
            lemma_and_lang = (one_dict["properties"]["fullLemma"], one_dict["properties"]["language"])
            node_lst.append(lemma_and_lang)
            # print("**********************************************")


print(node_lst)