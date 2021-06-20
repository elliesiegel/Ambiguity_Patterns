import sys
import re
import pickle
import json
from pathlib import Path

# Prep.
json_file_path = sys.argv[1]
dumpfile_path = sys.argv[2]

json_file_name = json_file_path.split('/')[-1]
name_part=json_file_name.split('_')

# Create or load query_dict
if Path(dumpfile_path).is_file():
    with open(dumpfile_path, 'rb') as f:
        query_dict = pickle.load(f)
else:
    query_dict = {}


# Recunstruct query urls
if name_part[-1]=="wordSenses.json":
    word='_'.join(name_part[0:-4])
    url = 'https://babelnet.io/v6/getSenses?lemma=' + word + '&searchLang=' + name_part[-4] + '&searchLang=' + name_part[-3] + '&searchLang=' + name_part[-2] + '&searchLang=EN&key=API_KEY'

if name_part[-1]=="wordsynsets.json":
    url = 'https://babelnet.io/v6/getSynset?id=' + name_part[0] + '&targetLang=' + name_part[-4] + '&targetLang=' + name_part[-3] + '&targetLang=' + name_part[-2] + '&targetLang=EN&key=API_KEY'

if name_part[-1]=="ids.json":
    json_file_name_normalized = re.sub('_DE_ES_FR','',json_file_name)
    json_file_name_normalized = re.sub('_RU_UK_PL','',json_file_name_normalized)
    json_file_name_normalized = re.sub('_CS_IT_NN','',json_file_name_normalized)
    word = '_'.join(json_file_name_normalized.split('_')[0:-2])
    url = 'https://babelnet.io/v6/getSynsetIds?lemma=' + word + '&searchLang=EN&key=API_KEY'


# Dump query dict
if url in query_dict:
    print('Existing query in dict: ', url)
else:
    print('Adding query number ', len(query_dict)+1,' dict: ', url)
    with open(json_file_path, "r") as f:
        query_dict[url]= json.load(f)

    with open(dumpfile_path, 'wb') as f:
        pickle.dump(query_dict, f)
