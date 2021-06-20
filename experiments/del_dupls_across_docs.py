import csv
import sys


# python3 del_dupls_across_docs.py all_4_cats_csv_bert-base/1_true_true.csv

input_1 = sys.argv[1]

def rm_duplicates_in_list(input_1):
    all_unique_words = set()
    with open(input_1) as csvfile_1:
        reader_1 = csv.reader(csvfile_1)
        for row in reader_1:
            all_unique_words.add(row[0])

    for word in all_unique_words:
        print(word)

rm_duplicates_in_list(input_1)


# def rm_duplicates_accross_docs(input_1):
#     input_2 = sys.argv[2]
#     input_3 = sys.argv[3]
#     input_4 = sys.argv[4]

#     with open(input_1) as csvfile_1, open(input_2) as csvfile_2, open(input_3) as csvfile_3, open(input_4) as csvfile_4:

#         file1 = csvfile_1.readlines()
#         file2 = csvfile_2.readlines()
#         file3 = csvfile_3.readlines()
#         file4 = csvfile_4.readlines()

#         # unique words from file1 that aren't in file2
#         # result = set(file1).difference(set(file2))
    
#         # print(len(result))
#         # print(result)

#         for word1 in file1:
#             for word2 in file2:
#                 if word1 == word2:
#                     print(word1, word2)

#                 for word3 in file3:
#                     if word1 == word3:
#                             print(word1, word3)
#                     for word4 in file4:
#                         if word1 == word4:
#                             print(word1, word4)


# rm_duplicates_accross_docs(input_1)