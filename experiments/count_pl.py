import csv
import sys


input_csv = sys.argv[1] # input file.csv with predictions false, false -- true, true

pl_words_set = set() 
all_words = set()
with open(input_csv) as csvfile:
    scv_reader = csv.reader(csvfile)
    for row in scv_reader:
        word = row[0]
        all_words.add(word)
        if word.endswith("s") and row[1] == "true":    # words plural and false
        # if row[1] == "true":
            pl_words_set.add(word)

print(pl_words_set)
# print(len(all_words))      
proper_names_false = ['United States Supreme Court', 'U.S.', 'Department of Energy', 'Fannie Mae', 'National Institutes of Health', 'Open University', 'Bush administration', 'San Jose', 'New York', 'Superior Court', 'Dow Jones', 'Code of Conduct', 'Washington', 'United States Senate', 'Central America', 'European countries', 'Costa Rica', 'World Cup', 'Wall Street', 'Supreme Court', 'Freddie Mac', 'South America', 'United Nations', 'European Union', 'Russia', 'New York Stock Exchange', 'Dominican Republic']
proper_names_true = ['Cleveland', 'Calif.', 'Peru', 'Venezuela', 'India', 'Mexico', 'Panama', 'Washington', 'NASA', 'Connecticut', 'France', 'Europe',  'China', 'Iraq', 'Israel', 'US', 'America', 'Brazil', 'NASDAQ', 'USA']
# print(len(proper_names_true))

# 668 words total
# 56 words plural right prediction by both models

# 140 plural words false prediction by both models
# total false prediction words: 364
# 27 proper names out of 364 total false preds

# 330 words correct prediciton
# 20 proper names out of 330 total correct preds

# problems with plurals for WSD
# problems with proper names: ['United States Supreme Court', 'U.S.', 'Department of Energy', 'Fannie Mae', 'National Institutes of Health', 'Open University', 'Bush administration', 'San Jose', 'New York', 'Superior Court', 'Dow Jones', 'Code of Conduct', 'Washington', 'United States Senate', 'Central America', 'European countries', 'Costa Rica', 'World Cup', 'Wall Street', 'Supreme Court', 'Freddie Mac', 'South America', 'United Nations', 'European Union', 'Russia', 'New York Stock Exchange', 'Dominican Republic']

# Problems with Proper Nouns or with Phrases, s. proper_names_false a lot of phrases
# no phrases in true predicred (always separate words) - proper_names_true