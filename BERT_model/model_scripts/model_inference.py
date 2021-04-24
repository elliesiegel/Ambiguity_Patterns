import argparse
import re

import torch
from tabulate import tabulate
from torch.nn.functional import softmax
from tqdm import tqdm
from transformers import BertTokenizer

from utils.dataset import GlossSelectionRecord, _create_features_from_records
from utils.model import BertWSD, forward_gloss_selection
from utils.wordnet import get_glosses

import sys 
import csv
import pandas as pd


def reader(file_name):
    data_csv = pd.read_csv(file_name)
    return data_csv

# file_name = sys.argv[1]
# df = reader(file_name)
# data_lst = df.values.tolist()


MAX_SEQ_LENGTH = 128
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_predictions(model, tokenizer, sentence):
    re_result = re.search(r"\[TGT\](.*)\[TGT\]", sentence)
    if re_result is None:
        print("\nIncorrect input format. Please try again.")
        return

    ambiguous_word = re_result.group(1).strip()
    sense_keys = []
    definitions = []
    for sense_key, definition in get_glosses(ambiguous_word, None).items():
        sense_keys.append(sense_key)
        definitions.append(definition)

    record = GlossSelectionRecord("test", sentence, sense_keys, definitions, [-1])
    features = _create_features_from_records([record], MAX_SEQ_LENGTH, tokenizer,
                                             cls_token=tokenizer.cls_token,
                                             sep_token=tokenizer.sep_token,
                                             cls_token_segment_id=1,
                                             pad_token_segment_id=0,
                                             disable_progress_bar=True)[0]

    with torch.no_grad():
        logits = torch.zeros(len(definitions), dtype=torch.double).to(DEVICE)
        for i, bert_input in tqdm(list(enumerate(features)), desc="Progress"):
            logits[i] = model.ranking_linear(
                model.bert(
                    input_ids=torch.tensor(bert_input.input_ids, dtype=torch.long).unsqueeze(0).to(DEVICE),
                    attention_mask=torch.tensor(bert_input.input_mask, dtype=torch.long).unsqueeze(0).to(DEVICE),
                    token_type_ids=torch.tensor(bert_input.segment_ids, dtype=torch.long).unsqueeze(0).to(DEVICE)
                )[1]
            )
        scores = softmax(logits, dim=0)

    return sorted(zip(sense_keys, definitions, scores), key=lambda x: x[-1], reverse=True)


def main():
    # file_name = sys.argv[1]
    # df = reader(file_name)
    # data_lst = df.values.tolist()

    parser = argparse.ArgumentParser()

    # Required parameters
    # parser.add_argument(
    #     "model_dir",
    #     default=None,
    #     type=str,
    #     help="Directory of pre-trained model."
    # )
    parser.add_argument(
        "file_name",
        default=None,
        type=str,
        help="name of the file with sentences and [TGT]-marked ambiguous words in them."
    )

    args = parser.parse_args()

    file_name = args.file_name
    df = reader(file_name)
    data_lst = df.values.tolist()

    # Load fine-tuned model and vocabulary
    print("Loading model...")
    # model = BertWSD.from_pretrained(args.model_dir)
    # tokenizer = BertTokenizer.from_pretrained(args.model_dir)

    model = BertWSD.from_pretrained("bert-base-uncased") # bert-base-multilingual-cased
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # example input german: ich liebe [TGT] Oktoberfest [TGT] und Bier
    # example input italian: Era un [TGT] capo [TGT] dell'organizzazione
    
    model.to(DEVICE)
    model.eval()

    for row in data_lst:
        sentence = row[1]
        glosses = row[3]
        print(">> ", sentence, " <<", "\n", "sentence glosses: ", glosses, "\n")
        predictions = get_predictions(model, tokenizer, sentence)
        if predictions:
            print("\nPredictions:")
            print(tabulate(
                [[f"{i+1}.", key, gloss, f"{score:.5f}"] for i, (key, gloss, score) in enumerate(predictions)],
                headers=["No.", "Sense key", "Definition", "Score"])
            )

            print("-"*30)
            print()

if __name__ == '__main__':
    main()
