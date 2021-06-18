# Ambiguity_Patterns

Master Thesis at Ludwig Maximilian University Munich (LMU). Project on **Word Ambiguity Detection with multilingual BERT** / Transformer architectures and pretrained models.  Data used in this project: https://babelnet.org/

# Dependencies:

```pip install -r requirements.txt```

change to the branch: *count_nodes_edges*


# Get the Inference of a Pre-Trained Model:

In the directory: *Ambiguity_Patterns/BERT_model/__model_scripts__/*

```python3 model_inference.py  directory_pretrained_model/  Input_Data/semeval2013.csv > model_inference_predictions.txt```


# Compute Accuracy of a Pre-Trained Model:

In the directory: *Ambiguity_Patterns/experiments*

```python3 compare_metrics.py Input_Data/semeval2013.csv model_inference_predictions.txt```



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
