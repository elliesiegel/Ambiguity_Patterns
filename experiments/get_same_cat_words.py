import re
import sys
from pathlib import Path


file_path = sys.argv[1]
p = Path(file_path)
files = list(p.glob('**/*.txt'))

to_be_compared_with = []
word_of_multiple_cats = []

def read_one(f):
    with open(f, "r") as txt:
        txt = txt.readlines()
        for word in txt:
            word = re.sub("\n", "", word)
            to_be_compared_with.append(word)


def get_same_words_from_cats(files, current_file):
    new_files = []
    # files.remove(current_file)
    for f in files:
        if f != current_file:
            new_files.append(f)

    for new_f in new_files:
        with open(new_f, "r") as txt:
            txt = txt.readlines()
            for word in txt:
                word = re.sub("\n", "", word)
                for word2 in to_be_compared_with:
                    if word == word2:
                        word_of_multiple_cats.append(word)

    return word_of_multiple_cats


current_file = files[2]
print("current file name -- ", current_file)
read_one(current_file)  # create a list of words to compare with
print()
word_of_multiple_cats_list = get_same_words_from_cats(files, current_file)
word_of_multiple_cats_list = set(word_of_multiple_cats_list)
print(list(word_of_multiple_cats_list))
print()
print("#"*20)

# def main():
#     for num in range(len(files)):
#         print(num, " ---- ", files)
#         current_file = files[num]
#         print("current file name -- ", current_file)
#         read_one(current_file)
#         print()
#         word_of_multiple_cats_list = get_same_words_from_cats(files, current_file)
#         print(word_of_multiple_cats_list)
#         print()
#         print("#"*20)

# main()
