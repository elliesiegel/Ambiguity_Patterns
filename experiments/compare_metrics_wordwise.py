import csv
import sys
import re

'''
generate result_bert.txt with create_preds_file.py
example call: python3 compare_metrics_wordwise.py ../Input_Data/semeval2013.csv ../result_bert.txt ../results_finetuned_mbert.txt results_bert_fine-tuned-mbert.csv

creates a csv with header = ["ambig word", "pred bert", "pred mbert", "true label"]
'''

data_csv = sys.argv[1]
path_to_bert = sys.argv[2]
path_to_mbert = sys.argv[3]
path_out_csv = sys.argv[4]

# with open(path_to_bert) as bert, open(path_to_mbert) as mbert:

#     data_bert = bert.readlines()
#     data_mbert = mbert.readlines()
    
#     num_preds = 0
#     for line in data_bert: # data_bert
#         if "[TGT]" in line:
#             bert_word = re.search(r"\[TGT\](.*)\[TGT\]", line)
#             ambiguous_word_bert = bert_word.group(1).strip()
#             print("ambig word: ", ambiguous_word_bert)
#         if "[SENT_1]" in line:
#             pred = re.sub("\[SENT_1\]", "", line)
#             pred = re.sub("\n", "", pred)
#             print("prediction: ", pred)
#             num_preds +=1
#             # print()
#         if "[ No Prediction for this sentence and this word ]" in line:
#             print("prediction: ", "no prediction")
#             num_preds +=1
#             # print()

# print(num_preds)

word_meaning_lst = []
all_words_list = []
all_meanings_true = []

def get_word_sense_dict(data_csv):
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

            sentence = row[1]
            word = re.search(r"\[TGT\](.*)\[TGT\]", sentence)
            ambiguous_word = word.group(1).strip()

            all_words_list.append(ambiguous_word)

            word_meaning_str = " ".join(word_meaning_lst)
            all_meanings_true.append(word_meaning_str)

    # word_sense_dict = {}
    # for amb_word in all_words_list:
    #     for meaning in all_meanings_true:
    #         word_sense_dict[amb_word] = meaning

    return all_words_list, all_meanings_true


def get_predictions(path_to_bert):
    with open(path_to_bert) as prediction:

        words = []
        preds = []
        # predicted_dict = {}
        data_prediction = prediction.readlines()
        
        for line in data_prediction:
            if "ambig word:" in line:
                word = re.sub("ambig word:  ", "", line)
                word = re.sub("\n", "", word)
                words.append(word)
            if "prediction:" in line:
                pred = re.sub("prediction:  ", "", line)
                pred = re.sub("\n", "", pred)
                preds.append(pred)
            
        # for word in words:
        #     for pred in preds:
        #         predicted_dict[word] = pred
            
    return words, preds


# word_sense_dict = get_word_sense_dict(data_csv) # TRUE dict
# preds = get_predictions(path_to_bert) # Predicted

# print(word_sense_dict)
# print(preds)

all_words_list, all_meanings_true = get_word_sense_dict(data_csv)   # TRUE
bert_words, bert_preds = get_predictions(path_to_bert)              # pred bert
mbert_words, mbert_preds = get_predictions(path_to_mbert)           # pred mbert

word_sense_lst = list(zip(*[all_words_list, bert_preds, mbert_preds, all_meanings_true]))

header = ["ambig word", "pred bert", "pred finetuned mbert", "true label"]

with open(path_out_csv, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for elem in word_sense_lst:
        word = elem[0]
        pred_sense_bert = elem[1]
        pred_sense_mbert = elem[2]
        true_label = elem[3]
        writer.writerow([word, pred_sense_bert, pred_sense_mbert, true_label])
