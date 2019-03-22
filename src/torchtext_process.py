# torch_text_process.py
# 2nd Mar. 2019
# IntSys-Summarization

import dill
import os

import torch
import torch.nn as nn
from torchtext import data, datasets

# CONSTANTS
SOS = 'SOS'
EOS = 'EOS'

FIELDS_ROOT_PATH = os.path.join("data", "fields")
SRC_FIELD_PATHS = ("src", os.path.join(FIELDS_ROOT_PATH, "src"))
TGT_FIELD_PATHS = ("src", os.path.join(FIELDS_ROOT_PATH, "src"))

def whitespace_tokenizer(text):
    return text.split(" ")

def load_torchtext_datasets(data_path, rel_train, rel_val, rel_test):
    if not os.path.exists(SRC_FIELD_PATHS[1]):
        SRC = data.Field(
                sequential = True,
                tokenize = whitespace_tokenizer,
                init_token = SOS,
                eos_token = EOS,
            )
    else:
        with open(SRC_FIELD_PATHS[1], 'rb') as dill_file:
            SRC = dill.load(dill_file)
        # Do we have to call build_vocab again? Because that would defeat the purp.

    if not os.path.exists(TGT_FIELD_PATHS[1]):
        TGT = data.Field(
                sequential = True,
                tokenize = whitespace_tokenizer,
                init_token = SOS,
                eos_token = EOS,
            )
    else:
        with open(TGT_FIELD_PATHS[1], 'rb') as dill_file:
            TGT = dill.load(dill_file)
        # Do we have to call build_vocab again? Because that would defeat the purp.

    train, val, test = data.TabularDataset.splits(
        path = data_path, train = rel_train, validation = rel_val, test = rel_test, 
        format='csv', fields=[(SRC_FIELD_PATHS[0], SRC), (TGT_FIELD_PATHS[0], TGT)])

    # Build SRC and TGT Vocab if not preloaded & save fields
    if not os.path.exists(SRC_FIELD_PATHS[1]):
        SRC.build_vocab(train) #TODO: Add vectors? How do we ensure that made-up-tokens are there?

        with open(SRC_FIELD_PATHS[1], 'wb') as dill_file:
            dill.dump(SRC, dill_file)

    if not os.path.exists(TGT_FIELD_PATHS[1]):
        TGT.build_vocab(train) #TODO: Add vectors? How do we ensure that made-up-tokens are there?

        with open(TGT_FIELD_PATHS[1], 'wb') as dill_file:
            dill.dump(TGT, dill_file)

    return (train, val, test), (SRC, TGT)
