import json
import urllib.request
import sys

# lemma=page --> lemma=word
# first argument "word" 
input_word = sys.argv[1]
print("*"*10)
print("initial word: ", "> ", input_word, " <")
print("*"*10)
# TODO: expand / change "searchLang=EN"
url = "https://babelnet.io/v6/getSynsetIds?lemma=[word]&searchLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
url = url.replace("[word]", input_word)
# print(url)
web_get_synset_ids = urllib.request.urlopen(url)
# response = web_get_synset_ids # redundant
data = json.load(web_get_synset_ids) 

# print(data)
# print(type(data))

# elem = id, pos, source
word_syns_ids = []
for elem in data:
    word_syns_ids.append(elem["id"]) # type dict

# idx = word_syns_ids[0]
# print(idx)
# url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
# url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
# web_get_synsets = urllib.request.urlopen(url_for_lemmas)
# print(web_get_synsets)

# import requests
# headers = {
#  'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
# }

for idx in word_syns_ids:
    # sometimes no senses is given, hence error "IndexError: list index out of range" occurs, so catching
    try:
        # id=bn:00091387v --> id=extracted_id from word_syns_ids
        url_for_lemmas = "https://babelnet.io/v6/getSynset?id=[synset_id]&targetLang=DE&targetLang=ES&targetLang=FR&targetLang=EN&key=299a9265-9746-4b40-a13f-b1cb0a7d3f1d"
        url_for_lemmas = url_for_lemmas.replace("[synset_id]", idx)
        web_get_synsets = urllib.request.urlopen(url_for_lemmas)
        # web_get_synsets = requests.get(url_for_lemmas)
        # print(web_get_synsets)
        data_synsets = json.load(web_get_synsets) 
        print(data_synsets["senses"][0]["properties"]["fullLemma"], data_synsets["senses"][0]["properties"]["language"]) 
        # and "language"
    except:
        pass


    # if data_synsets["language"]=="FR":
        # print(data_synsets)
    # for elem in data_synsets:
        # print(elem)
        # if elem["language"]=="FR":
        #     print(elem)
    