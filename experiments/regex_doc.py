import re
import sys


input_file = sys.argv[1]

def apply_regex(input_file):
    # pattern = "', [0-9]*, [0-9]*, false\).*$"
    # pattern = "^.*?\) - \('"
    pattern = "', [0-9]*, [0-9]*, true\).*$"

    with open(input_file) as f:
        f = f.readlines()
        for line in f:
            new_line = re.sub(pattern, "", line)
            new_line = re.sub("\n", "", new_line)
            # new_line = re.sub("\('", "", new_line)
        
            print(new_line)


def del_duplicates(input_file):
    word_set = set()
    with open(input_file) as f:
        f = f.readlines()
    for word in f:
        word = re.sub("\n", "", word)
        word_set.add(word)

    return word_set

word_set = del_duplicates(input_file)
print(word_set)

# for word in word_set:
#     print(word)