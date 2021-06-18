import sys
import re

'''
example call: 
python3 create_preds_file.py ../BERT_model/results_on_mBERT/inferred_on_semeval_test_2013/mbert_finetuned_chkpnt24000.txt > ../results_finetuned_mbert.txt

creates a file with a word and its sense prediction
'''

path_to_bert = sys.argv[1]

with open(path_to_bert) as bert: #, open(path_to_mbert) as mbert:

    data_bert = bert.readlines()
    # data_mbert = mbert.readlines()
    
    num_preds = 0
    for line in data_bert: # data_bert
        if "[TGT]" in line:
            bert_word = re.search(r"\[TGT\](.*)\[TGT\]", line)
            ambiguous_word_bert = bert_word.group(1).strip()
            print("ambig word: ", ambiguous_word_bert)
        if "[SENT_1]" in line:
            pred = re.sub("\[SENT_1\]", "", line)
            pred = re.sub("\n", "", pred)
            print("prediction: ", pred)
            num_preds +=1
            # print()
        if "[ No Prediction for this sentence and this word ]" in line:
            print("prediction: ", "no prediction")
            num_preds +=1
            # print()

# print(num_preds)
