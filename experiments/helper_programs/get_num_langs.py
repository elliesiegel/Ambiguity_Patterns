import glob
import json
import sys

# get number of languages
# get number of words in a clique

files_directory = sys.argv[1]
language_set = set()


def get_languages(files_directory):
    wordSenses = glob.glob(files_directory + "*_wordSenses.json")
    # wordSenses = glob.glob(files_directory + "*_wordsynsets.json")
    for f in wordSenses:
        with open(f) as document:
            json_doc = json.load(document)
            try:
                for a_dict in json_doc:
                    # print(a_dict["properties"]["fullLemma"], a_dict["properties"]["language"])
                    language_set.add(a_dict["properties"]["language"])
                # print(" ############# ")
            except:
                for a_dict in json_doc["senses"]:
                    print(a_dict["properties"]["fullLemma"], a_dict["properties"]["language"])
                    language_set.add(a_dict["properties"]["language"])


# get_languages(files_directory)
# print(len(language_set))
# print(language_set)

# 12
# {'RU', 'EN', 'IT', 'DE', 'UK', 'NO', 'NN', 'CS', 'PL', 'TR', 'ES', 'FR'}


# num of words in a clique
def get_num_words(files_directory, name_end_json):
    num_words = 0
    wordSenses = glob.glob(files_directory + name_end_json)
    # wordSenses = glob.glob(files_directory + "*_wordSenses.json")
    # wordSenses = glob.glob(files_directory + "*_wordsynsets.json")
    for f in wordSenses:
        with open(f) as document:
            json_doc = json.load(document)
            try:
                for a_dict in json_doc:
                    print(a_dict["properties"]["fullLemma"], a_dict["properties"]["language"])
                    num_words += 1
                    # language_set.add(a_dict["properties"]["language"])
                # print(" ############# ")
            except:
                for a_dict in json_doc["senses"]:
                    print(a_dict["properties"]["fullLemma"], a_dict["properties"]["language"])
                    num_words += 1
                    # language_set.add(a_dict["properties"]["language"])
        print("############################")
        print(num_words)
        print("############################")


get_num_words(files_directory, "*_wordsynsets.json")
