import re
import csv
import ast
import sys
import json


data_csv = sys.argv[1]

with open(data_csv) as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    for row in csv_reader:
        glosses = row[3]
        glosses = glosses.strip("[]")
        rx_comma = re.compile(r"(?<=')[^']*(?=})")
        glosses = rx_comma.split(glosses)
        glosses = glosses[0].split("'")
        glosses = [value for value in glosses if value != ', ']
        glosses_list = [value for value in glosses if value != '']
        # print(glosses_list)

        true_label_id = row[4]
        # print(true_label_id)
        true_label_ids = true_label_id.strip("[]").split()
        for idx in true_label_ids:
            idx = idx.strip(",")
            idx = idx.strip(" ")
            idx = int(idx)
            print(glosses_list[idx], idx) # TRUE labels for the words

# TODO save sentences from glosses_list[idx] in a list
# compare with sentences from results