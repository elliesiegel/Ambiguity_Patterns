import csv
import sys


input_csv = sys.argv[1]
input_csv_2 = sys.argv[2]
lst_1 = []
lst_2 = []

with open(input_csv) as csvfile, open(input_csv_2) as csvfile_2, open('new_all-trues_nodes_edges.csv', 'w') as new_csv:
    reader = csv.reader(csvfile)
    reader_2 = csv.reader(csvfile_2)
    for row in reader:
        lst_1.append(row[0])
        for row_2 in reader_2:
            lst_2.append(row_2[0])
            # if row[0] == row_2[0]:
            # print(row[0], row_2[0])

            # writer = csv.writer(new_csv)
            # # write a row to the csv file
            # writer.writerow(row) 

print(set(lst_1).intersection(lst_2))



#input_csv = sys.argv[1]

# with open(input_csv) as csvfile, open('falses.csv', 'w') as false:
#     reader = csv.reader(csvfile)
#     next(reader)
#     for row in reader:
#         if row[1] == 'false' and row[2] == 'false':
            
#             writer = csv.writer(false)
#             # write a row to the csv file
#             writer.writerow(row) 


# import csv
# import sys
# import os


# input_csv = sys.argv[1]
# del_dups = set()

# with open(input_csv) as csvfile, open('2_trues.csv', 'w') as false:
#     reader = csv.reader(csvfile)
#     next(reader)
#     for row in reader:
#         del_dups.add(row[0])

#     writer = csv.writer(false)
#     # write a row to the csv file
#     for word in del_dups:
#         writer.writerow([word, "true", "true"]) 


# input_csv = sys.argv[1]
# del_dups = set()

# with open(input_csv) as csvfile:
#     reader = csv.reader(csvfile)
#     # next(reader)
#     for row in reader:
#         del_dups.add(row[0])

# dir_names = os.listdir('/home/ellie/Desktop/MA/Ambiguity_Patterns/experiments/JSON_data_comparison/both_ture')
# # print(type(dir_names))
# for word in del_dups:
#     for word2 in dir_names:
#         if word == word2:
#             print(word)

# trues:
# country
# climate
# case

# falses:
# assumption
# card
# charges
# release
# Appeal
# cases
# benefit
# cards
# challenges
# text
# beds
# analysts
# advantage
# challenge
# case
# budgets
# absences
# action
# chemical
# boost
# arguments
# chart
# acts
# barrel
# bid
# advance
# club
# circumstances
# breach
# closing
# circles
# argument
# actions
# area
