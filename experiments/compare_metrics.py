import re
import csv
import ast
import sys
import json
import pandas as pd

# example call: python3 compare_metrics.py Input_Data/semeval2013.csv results_on_mBERT/inferred_on_semeval_test_2013/multilingual_BERT.txt
'''
calculates accuracy for the overall prediction
'''

data_csv = sys.argv[1]
result_file = sys.argv[2]

pred_label_lst = []

cnt_true = 0
all_meanings_true = []

with open(data_csv) as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    for row in csv_reader:
        # glosses
        glosses = row[3]
        glosses_list = eval(glosses) 
        glosses_true_id = [int(t) for t in eval(row[4])] # true ids
        word_meaning_lst = []
        if len(glosses_true_id) > 1:
            for idx in glosses_true_id:
                word_meaning_lst.append(glosses_list[idx])
        else:
            word_meaning_lst.append(glosses_list[glosses_true_id[0]])

        word_meaning_str = " ".join(word_meaning_lst)
        all_meanings_true.append(word_meaning_str)


cnt_preds = 0
cnt_no_preds = 0
with open(result_file) as result_file:
    result_file_reader = result_file.readlines()
    for line in result_file_reader:
        if "[SENT_1]" in line:
            line = re.sub("\[SENT_1\]", "", line)
            line= re.sub("\n", "", line)
            cnt_preds += 1
            pred_label_lst.append(line)
            # print(line)
        if "[ No Prediction for this sentence and this word ]" in line:
            # print("Not predicted/ignored")
            line= re.sub("\n", "", line)
            pred_label_lst.append(line)
            cnt_preds += 1
            cnt_no_preds += 1

# print(len(all_meanings_true))
# print(len(pred_label_lst))

compare_data = {"predicted": pred_label_lst, "true labels": all_meanings_true}
df_compare_data = pd.DataFrame(compare_data)
# print(df_compare_data)

cnt_all_preds = 0
cnt_corrects = 0
cnt_falses = 0
for i, row in df_compare_data.iterrows():
    pred = row[0]
    true = row[1]

    cnt_all_preds += 1
    if pred.find(true) != -1:
        cnt_corrects += 1
        # print(pred.find(true))
    else:
        cnt_falses += 1
        print("false preds: ", pred, " ------ ", true)  
         
print()
print("no predictions: ", cnt_no_preds)
print("all preds: ", cnt_all_preds)
print()
totals_ignored_no_preds = cnt_all_preds - cnt_no_preds
print("ignore no predictions / total predictions: ", totals_ignored_no_preds)
print("correct: ", cnt_corrects)
print("false: ", cnt_falses - cnt_no_preds)
print()
# accuracy = (correctly predicted class / total testing class) × 100%
print("accuracy: ", (cnt_corrects / totals_ignored_no_preds)*100, " %")


# Datatset SE13  (semeval2013):
#
# bert_large-augmented-batch_size\=128-lr\=2e-5-max_gloss\=6:
# no predictions:  128
# all preds:  1644

# ignore no predictions / total predictions:  1516
# correct:  916
# false:  600

# accuracy:  60.4221635883905  %


# bert base:
# no predictions:  128
# all preds:  1644

# ignore no predictions / total predictions:  1516
# correct:  861
# false:  655

# accuracy:  56.79419525065963  %


# mBERT:
# no predictions:  128
# all preds:  1644

# ignore no predictions / total predictions:  1516
# correct:  506
# false:  1010

# accuracy:  33.37730870712401  %


# mBERT fine tuned on WSD (training data: semcor-max_num_gloss=6-augmented.csv)
# no predictions:  128
# all preds:  1644

# ignore no predictions / total predictions:  1516
# correct:  700
# false:  816

# accuracy, 1 epoch:  46.17414248021108  %
# acc, 2 epochs: 50.065963060686016 % 
