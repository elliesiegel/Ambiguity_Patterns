import argparse
import csv

'''
categorizes word's sentences into 4 categories for mbert and bert

true, true
false, false
true, false
false, true

call: python3 categorize.py results_model1_model2.csv false_false.csv --false_false
'''

parser = argparse.ArgumentParser()

parser.add_argument(
    "input_file_csv",
    default=None,
    type=str,
    help="csv with -- ambig word,pred bert,pred mbert,true label -- "
)
parser.add_argument(
    "output_file_csv",
    default=None,
    type=str,
    help="output csv with ambig word, true or false pred for models "
)

parser.add_argument(
    "--true_true",
    action='store_true',
    help="both models predicted correctly"
)

parser.add_argument(
    "--true_false",
    action='store_true',
    help="bert correct - mbert false"
)

parser.add_argument(
    "--false_true",
    action='store_true',
    help="bert false - mbert correct"
)

parser.add_argument(
    "--false_false",
    action='store_true',
    help="both models predicted falsely"
)


parser.add_argument(
    "--monolingual",
    action='store_true',
    help="only words from BERT predicted correctly"
)

parser.add_argument(
    "--multilingual",
    action='store_true',
    help="only words from multilingual BERT predicted correctly"
)

parser.add_argument(
    "--multi_false",
    action='store_true',
    help="only words from multilingual BERT predicted falsely"
)


args = parser.parse_args()

input_file_csv = args.input_file_csv
output_csv = args.output_file_csv

true_true = args.true_true
true_false = args.true_false
false_true = args.false_true
false_false = args.false_false

mono = args.monolingual
multi = args.multilingual
multi_false = args.multi_false

with open(input_file_csv) as csvfile, open(output_csv, 'w', encoding='UTF8') as cats:

    writer = csv.writer(cats)
    header = ["ambig word", "pred bert", "pred mbert"] #, "num nodes", "num edges", "pattern"]
    writer.writerow(header)

    csv_reader = csv.reader(csvfile)
    # csv row: "ambig word", "pred bert", "pred mbert", "true label"
    for row in csv_reader:
        ambig_word = row[0]
        pred_bert = row[1]
        pred_mbert = row[2]
        true_label = row[3]

        if true_true:
            if pred_bert == true_label and pred_mbert == true_label:
                writer.writerow([ambig_word, "true", "true"])  

        if false_false:
            if pred_bert != true_label and pred_mbert != true_label:
                writer.writerow([ambig_word, "false", "false"])
        
        if false_true:
            if pred_bert != true_label and pred_mbert == true_label:
                writer.writerow([ambig_word, "false", "true"])
    
        if true_false:
            if pred_bert == true_label and pred_mbert != true_label:
                writer.writerow([ambig_word, "true", "false"])

        if mono:
            if pred_bert == true_label:
                writer.writerow([ambig_word, "bert true", "-"])
                

        if multi:
            if pred_mbert == true_label:
                writer.writerow([ambig_word, "-", "mbert true"])
        
        if multi_false:
            if pred_mbert != true_label:
                writer.writerow([ambig_word, "-", "mbert false"])