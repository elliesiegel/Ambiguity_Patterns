# conda activate wordembed_env
import re
import sys
import time

from lxml import etree as et
from tqdm import tqdm

import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
 
from gensim.models.fasttext import FastText
from gensim.models import Word2Vec

# Custom:
from reduce_dims_viz import tsne_plot 

# nltk.download()

'''
example program call: >> python3 word_embeds.py path/to/word_file

conda activate wordembed_env
'''

start_time = time.time()
input_words_txt = sys.argv[1]

def file_reader(input_words_txt):
    with open(input_words_txt) as text:
        text = text.readlines()
    
    return text


def cleaner(word_lst):
    unique_words = set()
    new_lst_of_wordlst = []
    for word in word_lst:
        word = re.sub(',', '', word)
        word = re.sub('\n', '', word)
        unique_words.add(word)
    for word in unique_words:
        word = [word]
        new_lst_of_wordlst.append(word)
    
    return new_lst_of_wordlst

word_lst = file_reader(input_words_txt)
word_tokens = cleaner(word_lst)

# word_tokens = [word_tokenizer.tokenize(sent) for sent in tqdm(clean_corpus)]

# find out total number of words:
# lengths = []
# for lst in word_tokens:
#     lengths.append(len(lst))
# print("total words: ", sum(lengths))

# FastText word embeddings support both Continuous Bag of Words (CBOW) and Skip-Gram models. 
# The gensim FastText class expects lists-of-words
# Here: fastText word embeddings for Skip-Gram
embedding_size = 300
window_size = 5
min_word_freq = 1
down_sampling = 1e-2

fast_Text_model = FastText(word_tokens,
                      size=embedding_size,
                      window=window_size,
                      min_count=min_word_freq,
                      sample=down_sampling,
                      workers=4,
                      sg=1,
                      iter=100)
print("FastText model training time: ", time.time() - start_time)

# Save fastText gensim model
model_path = "embed_model/fasttext_embed_model"
fast_Text_model.save(model_path)

# Load saved gensim fastText model
fast_Text_model = Word2Vec.load(model_path)

# Print a word embedding for a particular word
word = "page"
embedding = fast_Text_model.wv[word]
print("page WordEmbedding : ")
print(embedding)
print()

print("Most similar words to the word: ", word)
most_sim = fast_Text_model.wv.most_similar(word, topn=10)
print(most_sim)

# Most opposite to a word
# fast_Text_model.wv.most_similar(negative=[word], topn=10)

print("---total time: %s seconds ---" % (time.time() - start_time))

# Visualize 
# tsne plot for top 10 similar word to "Auswertungsmethoden"
tsne_plot(for_word=word, w2v_model=fast_Text_model)


'''
Update pre-trained Gensim fastText model
'''
# new_data = [['yes', 'this', 'is', 'the', 'word2vec', 'model'],[ 'if',"you","have","think","about","it"]]
# # Update trained gensim fastText model
# fast_Text_model.build_vocab(new_data, update=True)
# # Update gensim fastText model using new data
# new_model = fast_Text_model.train(new_data, total_examples=fast_Text_model.corpus_count, epochs=fast_Text_model.iter)
