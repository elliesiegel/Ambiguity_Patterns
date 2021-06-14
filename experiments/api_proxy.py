import json
import urllib.request
import pickle
from pathlib import Path


class ApiProxy():

    def __init__(self, dumpfile_path):
        self.dumpfile_path = dumpfile_path
        if Path(self.dumpfile_path).is_file():
            with open(self.dumpfile_path, 'rb') as f:
                self.query_dict = pickle.load(f)
        else:
            self.query_dict = {}

    def query_for_json(self, url):
        if url not in self.query_dict:
            web_get_synset_ids = urllib.request.urlopen(url)
            json_reply=json.load(web_get_synset_ids)
            if "Your key is not valid or the daily requests limit has been reached." in json_reply:
                print("NO DUMP DUE TO: Your key is not valid or the daily requests limit has been reached.")
                return json_reply
            else:
                self.query_dict[url]=json_reply
        return self.query_dict[url]

    def query_dump(self):
        with open(self.dumpfile_path, 'wb') as f:
            pickle.dump(self.query_dict, f)
        print("Stored for BabelNet Queries in ", self.dumpfile_path)



# Test of ApiProxy class
# import sys

# proxy=ApiProxy('test.dump')
# print(proxy.query_for_json(sys.argv[1]))
# proxy.query_dump()