Run the __crawler-babelnet.sh__ for each of the categories to acquire average data for ambiguity graphs. You can find an example to run the script for all categories at once in the file *run_all_cats.sh*

```./crawler-babelnet.sh dir_with_cats/category/input_cat_words.txt save_res_dir/category/ API_KEY```


Categories:

*TT* - both models predcited the sense of the word correctly

*FF* - both models predcited the sense of the word incorrectly

*FT* - BERT predicted the sense incorrectly, mBERT correctly

*TF* - BERT predicted the sense correctly, mBERT incorrectly


*monolingual_correct* - all words BERT predicted correctly

*monolingual_incorrect* - all words BERT predicted incorrectly


*multilingual_correct* - all words mBERT predicted correctly

*multilingual_incorrect* - all words mBERT predicted incorrectly


Output are the following directories:

- __words__: json graph information per word
- __RESULTS_figure_CSV__: contains graph pngs and the stats file *word-nodes-edges.csv*
- __get_pattern_synsets-output__: intermediate results for word graphs per word
- __get_sense_graph_output__: intermediate results for sense graphs per word


In the directory __RESULTS_figure_CSV__ the file *word-nodes-edges.csv* can be found where all metrics for an ambiguity graph are collected. The same is for monolingual configuration (BERT).


**Get Agerage Results per Category**

Use the file *get_average.py* in the __helper_programs__ directory.

``` python3 get_average.py cat_data/category/RESULTS_figure_CSV/word-nodes-edges.csv ```