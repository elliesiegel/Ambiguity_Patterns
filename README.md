# Ambiguity_Patterns

Master Thesis at Ludwig Maximilian University Munich (LMU). Project on **Word Ambiguity Detection with multilingual BERT** / Transformer architectures and pretrained models.  Data used in this project: https://babelnet.org/

# Dependencies:

```pip install -r requirements.txt```


# Get the Inference of a Pre-Trained Model:

In the directory: *Ambiguity_Patterns/BERT_model/__model_scripts__/*

```python3 model_inference.py  directory_pretrained_model/  Input_Data/semeval2013.csv > model_inference_predictions.txt```


[directory_pretrained_model](https://entuedu-my.sharepoint.com/personal/boonpeng001_e_ntu_edu_sg/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fboonpeng001%5Fe%5Fntu%5Fedu%5Fsg%2FDocuments%2FBERT%2DWSD%2Fmodel&originalPath=aHR0cHM6Ly9lbnR1ZWR1LW15LnNoYXJlcG9pbnQuY29tLzpmOi9nL3BlcnNvbmFsL2Jvb25wZW5nMDAxX2VfbnR1X2VkdV9zZy9FZ3B0NzdFYW1ncEVsOXNPOTBGc3RyWUI1cHMxTzB2c0hVQTRGZnB6ZlZqNnZBP3J0aW1lPVhINnl3bkV5MlVn)

[semeval2013.csv](https://entuedu-my.sharepoint.com/personal/boonpeng001_e_ntu_edu_sg/_layouts/15/onedrive.aspx?originalPath=aHR0cHM6Ly9lbnR1ZWR1LW15LnNoYXJlcG9pbnQuY29tLzpmOi9nL3BlcnNvbmFsL2Jvb25wZW5nMDAxX2VfbnR1X2VkdV9zZy9Fc2RGQ1doQXdpNU90MEl0Qk9TazNVRUJLOEZVd2xNU2lfalNyQk42RnJHcWh3P3J0aW1lPUNURkY2WEV5MlVn&id=%2Fpersonal%2Fboonpeng001%5Fe%5Fntu%5Fedu%5Fsg%2FDocuments%2FBERT%2DWSD%2Fdata%2Ftest)

# Compute Accuracy of a Pre-Trained Model:

In the directory: *Ambiguity_Patterns/experiments*

```python3 compare_metrics.py Input_Data/semeval2013.csv model_inference_predictions.txt```


# Get Word Categories of BERT vs. mBERT

```python3 create_preds_file.py model_inference_predictions.txt > ambig_word-prediction_results.txt```

__ambig_word-prediction_results.txt__:

*ambig word:  group*

*prediction:  any number of entities (members) considered as a unit*


```python3 compare_metrics_wordwise.py Input_Data/semeval2013.csv model1_ambig_word-prediction_results.txt model2_ambig_word-prediction_results.txt dir_to_save/results_model1_model2.csv```

__results_model1_model2.csv__:

*ambig word, pred bert, pred mbert, true label*

```python3 categorize.py results_model1_model2.csv false_false.csv --false_false```

```python3 categorize.py results_model1_model2.csv false_true.csv --false_true```

```python3 categorize.py results_model1_model2.csv true_false.csv --true_false```

```python3 categorize.py results_model1_model2.csv true_true.csv --true_true```

*for multilingual vs monolingual comparison do:*

```python3 categorize.py results_model1_model2.csv multilingual_true.csv --multi```

```python3 categorize.py results_model1_model2.csv monolingual_true.csv --mono```


For the *categorize.py* file see *helper_programs/categorize.py*


**Data Collection Pipeline**:

In order to collect word data ambiguity graphs, we construct a data pipeline.

```./crawler-babelnet.sh category/word_list.txt where_to_save_data/category/ API_KEY```


In the file *run_all_cats.sh* example calls can be found to run the *crawler-babelnet.sh* script for each category at once (s. *experiments/run_all_cats.sh* as well as *experiments/crawler-babelnet.sh*).

In each category *(TT/TF/FT/FF for BERT and mBERT predictions of word senses)* we create directories where we save multilingual ambiguity graphs as well as monolingual ambiguity graph information.

We also create a directory called *words* where all words' graph information is stored in a json format.

The results are saved in *word-nodes-edges.csv* and *word-nodes-edges-monolingual.csv* files that have the following graph information per each line:

*word, num nodes, num edges, num clique nodes, num clique-edges, var clique-weights, var clique-edges weights*


**References**:

[How multilingual is Multilingual BERT?](http://www.dhgarrette.com/papers/pires_multilingual_bert_acl2019.pdf)

[GlossBERT: BERT for Word Sense Disambiguation with Gloss Knowledge](https://arxiv.org/pdf/1908.07245.pdf)

[GutHub Repo for GlossBERT](https://github.com/HSLCY/GlossBERT)

[Adapting BERT for Word Sense Disambiguation with Gloss Selection Objective and Example Sentences](https://arxiv.org/abs/2009.11795)

[GitHub Repo for Adapting BERT for WSD](https://github.com/BPYap/BERT-WSD)

[Adapting BERT for WSD DATA](https://entuedu-my.sharepoint.com/personal/boonpeng001_e_ntu_edu_sg/_layouts/15/onedrive.aspx?originalPath=aHR0cHM6Ly9lbnR1ZWR1LW15LnNoYXJlcG9pbnQuY29tLzpmOi9nL3BlcnNvbmFsL2Jvb25wZW5nMDAxX2VfbnR1X2VkdV9zZy9Fc2RGQ1doQXdpNU90MEl0Qk9TazNVRUJLOEZVd2xNU2lfalNyQk42RnJHcWh3P3J0aW1lPWtnbF9tRF83MkVn&id=%2Fpersonal%2Fboonpeng001%5Fe%5Fntu%5Fedu%5Fsg%2FDocuments%2FBERT%2DWSD%2Fdata)

[Identifying Elements Essential for BERT’s Multilinguality](https://arxiv.org/pdf/2005.00396.pdf)

[Unsupervised Cross-lingual Representation Learning at Scale Alexis Conneau](https://www.aclweb.org/anthology/2020.acl-main.747.pdf)

[Does BERT Make Any Sense? Interpretable Word Sense Disambiguation with Contextualized Embeddings](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2019-wiedemannetal-bert-sense.pdf)

[mBERT](https://github.com/google-research/bert/blob/master/multilingual.md)

[Word Sense Disambiguation using BERT, ELMo and Flair](https://github.com/uhh-lt/bert-sense) _s. "Does BERT Make Any Sense?"_

[SENSEMBERT: Context-Enhanced Sense Embeddings for Multilingual Word Sense Disambiguation](http://sensembert.org/resources/scarlini_etal_aaai2020.pdf)

[Context-Enhanced Sense Embeddings for Multilingual Word Sense](http://sensembert.org/)

[With More Contexts Comes Better Performance: Contextualized Sense Embeddings for All-Round Word Sense Disambiguation](https://www.aclweb.org/anthology/2020.emnlp-main.285.pdf)

[XL-WiC: A Multilingual Benchmark for Evaluating Semantic Contextualization](https://arxiv.org/pdf/2010.06478.pdf)

[Train-O-Matic: Large-Scale Supervised Word Sense Disambiguation in Multiple Languages without Manual Training Data](https://www.aclweb.org/anthology/D17-1008.pdf)

[Word Sense Disambiguation: A Survey ROBERTO NAVIGLI Universita di Roma La Sapienza](http://wwwusers.di.uniroma1.it/~navigli/pubs/ACM_Survey_2009_Navigli.pdf)

[1] [Navigli, R., & Ponzetto, S. P. (2012). BabelNet: The automatic
construction, evaluation and application of a wide-coverage multilingual
semantic network. Artificial Intelligence, 193, 217-250.](http://wwwusers.di.uniroma1.it/~navigli/pubs/AIJ_2012_Navigli_Ponzetto.pdf)

[2] Agirre, E., López de Lacalle, O., & Soroa, A. (2014). Random walks
for knowledge-based word sense disambiguation. Computational
Linguistics, 40(1), 57-84.

[3] Navigli, R., Jurgens, D., & Vannella, D. (2013). Semeval-2013 task
12: Multilingual word sense disambiguation. In Second Joint Conference
on Lexical and Computational Semantics (* SEM), Volume 2: Proceedings of
the Seventh International Workshop on Semantic Evaluation (SemEval 2013)
(Vol. 2, pp. 222-231).

[4] Iacobacci, I., Pilehvar, M. T., & Navigli, R. (2016). Embeddings for
word sense disambiguation: An evaluation study. In Proceedings of the
54th Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers) (Vol. 1, pp. 897-907)
