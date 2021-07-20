#!/bin/bash

# Example to call on all 8 categories:
# ./crawler-babelnet.sh dir_with_cats/category/input_cat_words.txt save_res_dir/category/ API_KEY

# Call Examples:
# - 4 binary categories:
./crawler-babelnet.sh JSON_FINAL/true_true/input_cat_words.txt JSON_FINAL/true_true/ API_KEY
./crawler-babelnet.sh JSON_FINAL/false_true/input_cat_words.txt JSON_FINAL/false_true/ API_KEY
./crawler-babelnet.sh JSON_FINAL/true_false/input_cat_words.txt JSON_FINAL/true_false/ API_KEY
./crawler-babelnet.sh JSON_FINAL/false_false/input_cat_words.txt JSON_FINAL/false_false/ API_KEY

# - BERT's prediction correct/incorrect:
./crawler-babelnet.sh JSON_FINAL/monolingual_false/input_cat_words.txt JSON_FINAL/monolingual_false/ API_KEY
./crawler-babelnet.sh JSON_FINAL/monolingual/input_cat_words.txt JSON_FINAL/monolingual/ API_KEY

# - mBERT's prediction correct/incorrect:
./crawler-babelnet.sh JSON_FINAL/multilingual_false/input_cat_words.txt JSON_FINAL/multilingual_false/ API_KEY
./crawler-babelnet.sh JSON_FINAL/multilingual/input_cat_words.txt JSON_FINAL/multilingual/ API_KEY
