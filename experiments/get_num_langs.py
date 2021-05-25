import glob
import json
import sys


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


get_languages(files_directory)
print(len(language_set))
print(language_set)

# 12
# {'RU', 'EN', 'IT', 'DE', 'UK', 'NO', 'NN', 'CS', 'PL', 'TR', 'ES', 'FR'}
