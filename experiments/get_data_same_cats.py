'''
s. get_data_same_cats.py:
false_false = ['ministry', 'president', 'time', 'impact', 'pound', 'conference', 'policy', 'U.S.', 'law', 'debate', 'bid', 'case', 'occasion', 'employment', 'return', 'period', 'state', 'lot', 'pressure', 'country', 'team', 'judge', 'world', 'democracy', 'generosity', 'end', 'Right', 'spirit', 'trial', 'region', 'sense', 'notion', 'action', 'market', 'record', 'challenge', 'start', 'deal', 'phase', 'level', 'life', 'discovery', 'question', 'argument', 'study', 'law', 'life', 'case', 'climate', 'Congress', 'output', 'possibility', 'hour', 'speculation', 'trial', 'experience', 'country', 'pressure', 'Washington', 'world', 'planet', 'research', 'fraud', 'policy', 'part', 'war', 'day', 'spirit', 'performance', 'team', 'action', 'levels', 'region', 'view', 'mood', 'region', 'program', 'discovery', 'U.S.', 'team', 'years', 'analysts', 'world', 'life', 'part', 'action', 'question', 'time', 'game', 'points', 'wages', 'members', 'business', 'number', 'sport', 'policy', 'Left']
true_true = ['court', 'dollar', 'crisis', 'labor', 'immigration', 'policy', 'USA', 'news', 'law', 'event', 'example', 'case', 'money', 'pressure', 'company', 'year', 'country', 'team', 'world', 'suit', 'atmosphere', 'spirit', 'trial', 'term', 'region', 'month', 'report', 'way', 'role', 'phosphorus', 'action', 'arsenic', 'elements', 'burden', 'process', 'life', 'compensation', 'experience', 'possibility', 'spirit', 'planet', 'question', 'country', 'life', 'speculation', 'action', 'Washington', 'output', 'levels', 'law', 'discovery', 'day', 'climate', 'region', 'performance', 'Congress', 'argument', 'hour', 'trial', 'team', 'research', 'fraud', 'part', 'case', 'policy', 'pressure', 'world', 'war', 'study', 'decision', 'region', 'discovery', 'practice', 'team', 'world', 'news', 'life', 'part', 'action', 'report', 'claim', 'question', 'policy', 'group', 'arsenic', 'example']
print(set(false_false).intersection(true_true))
'''

import re
import sys
import csv


in_concat_file = sys.argv[1]

# words in both false-false and true-true - len 32:
words_both_FF_TT = ['experience', 'planet', 'spirit', 'Congress', 'life', 'case', 'question', 'speculation', 'study', 'hour', 'possibility', 'research', 'action', 'part', 'policy', 'performance', 'country', 'team', 'trial', 'levels', 'discovery', 'argument', 'fraud', 'world', 'day', 'region', 'climate', 'pressure', 'Washington', 'output', 'war', 'law']

# word in both true-false and false.true - len 19:
words_both_TF_FT = ['news', 'issue', 'life', 'world', 'policy', 'example', 'World', 'arsenic', 'team', 'degree', 'dinner', 'time', 'addition', 'report', 'work', 'outcome', 'U.S.', 'region', 'action']

all_multiple_cats_words = words_both_FF_TT + words_both_TF_FT
all_multiple_cats_words = set(all_multiple_cats_words)
# 51 total words in different categories

def get_ambig_graph_data(in_concat_file, words_mult_cats): 
    with open(in_concat_file) as graph_data:
        graph_data_reader = csv.reader(graph_data)
        for row in graph_data_reader:
            ambig_word = row[0]
            for word in words_mult_cats:
                if ambig_word == word:
                    print(', '.join(row))

# get_ambig_graph_data(in_concat_file, all_multiple_cats_words)


# very similar num of nodes/edges in sense graphs, but diff preds
true_preds = {'matter', 'reductions', 'economists', 'prosecutors', 'law', 'investors', 'immigrants', 'Immigration', 'responsiveness', 'waiters', 'intention', 'ruling', 'discovery', 'firm', 'proposal', 'height', 'poverty', 'culpability', 'election', 'imperative', 'lawyer', 'heading', 'banalities', 'reporting', 'Nicaragua', 'verdict', 'ethos', 'cameras', 'hordes', 'risks'}
false_preds = {'auctions', 'growth', 'hard_time', 'courts', 'justices', 'acceptance', 'Freddie_Mac', 'speculation', 'National_Institutes_of_Health', 'narrow_margin', 'obligations', 'spite', 'photographs', 'Department_of_Energy', 'advance', 'tone', 'deal', 'New_York_Stock_Exchange', 'appearance', 'things', 'life_forms', 'robustness', 'violence', 'publication'}


def csv_reader(in_concat_file, words_in_to_comp):
    with open(in_concat_file) as graph_data:
        graph_data_reader = csv.reader(graph_data)
        for row in graph_data_reader:
            ambig_word = row[0]
            for word in words_in_to_comp:
                if ambig_word == word:
                    print(', '.join(row))


csv_reader(in_concat_file, true_preds)