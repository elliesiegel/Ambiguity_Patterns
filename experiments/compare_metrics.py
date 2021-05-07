import re
import csv
import ast
import sys
import json


data_csv = sys.argv[1]
result_file = sys.argv[2]

cnt_true = 0
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
            cnt_true += 1
            # print(glosses_list[idx], idx) # TRUE labels for the words

# TODO save sentences from glosses_list[idx] in a list
# compare with sentences from results


cnt_preds = 0
with open(result_file) as result_file:
    result_file_reader = result_file.readlines()
    for sent_symbols in result_file_reader:
        found_sentence = re.search(r"\[SENT\](.*)\[SENT\]", sent_symbols)
        if found_sentence is not None:
            found_sentence = found_sentence.group(1).strip()
            found_sentence = re.sub("[SENT] ", "", found_sentence)
            print(found_sentence)
            cnt_preds += 1

print(cnt_true)
print(cnt_preds)
