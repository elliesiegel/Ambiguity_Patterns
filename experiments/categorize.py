import csv
import sys

'''
categorizes word's sentences into 4 categories for mbert and bert

true, true
false, false
true, false
false, true
'''

data_csv = sys.argv[1]

with open(data_csv) as csvfile, open("categories.csv", 'w', encoding='UTF8') as cats:

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

        if pred_bert == true_label and pred_mbert == true_label:
            writer.writerow([ambig_word, "true", "true"])  

        if pred_bert != true_label and pred_mbert != true_label:
            writer.writerow([ambig_word, "false", "false"])
        
