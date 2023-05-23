# -*- coding: utf-8 -*-
import json
import torch
from tqdm import tqdm
from transformers import BertTokenizer, BertForSequenceClassification, BertTokenizerFast, AutoModelForSequenceClassification
from torch.utils.data import DataLoader, Dataset

"""
  setup
"""
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TOKENIZER = BertTokenizerFast.from_pretrained("bert-base-chinese")
STANCE_MODEL = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=3).to(DEVICE)
SENTIMENT_MODEL = BertForSequenceClassification.from_pretrained("ckiplab/bert-tiny-chinese",num_labels=3).to(DEVICE)

def setup():
  model_path = "stance_model/pytorch_model.bin"
  state_dict = torch.load(model_path, map_location=DEVICE)
  STANCE_MODEL.load_state_dict(state_dict)
  model_path = "sentiment_model/pytorch_model.bin"
  state_dict = torch.load(model_path, map_location=DEVICE)
  SENTIMENT_MODEL.load_state_dict(state_dict)

class StanceDataset(Dataset):
    def __init__(self, inputs, tokenized_inputs, labels):
        #self.split = split
        self.inputs = inputs
        self.tokenized_inputs = tokenized_inputs
        self.labels = [label + 1 for label in labels]
        
        self.max_input_len = 50
        # Input sequence length = [CLS] + input + [SEP]
        self.max_seq_len = 1 + self.max_input_len + 1
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        inputs = self.inputs[idx]
        tokenized_inputs = self.tokenized_inputs[idx]
        label = self.labels[idx]
        # Add special tokens (101: CLS, 102: SEP)
        input_ids = [101] + tokenized_inputs.ids[:self.max_input_len] + [102]
        input_ids, token_type_ids, attention_mask = self.padding(input_ids)
        return torch.tensor(input_ids), torch.tensor(token_type_ids), torch.tensor(attention_mask), torch.tensor(label)

    def padding(self,input_ids):
        # Pad zeros if sequence length is shorter than max_seq_len
        padding_len = self.max_seq_len - len(input_ids)
        
        token_type_ids = [1] * len(input_ids) + [0] * padding_len
        attention_mask = [1] * len(input_ids) + [0] * padding_len
        input_ids = input_ids + [0] * padding_len
        return input_ids, token_type_ids, attention_mask

class SentimentDataset(Dataset):
    def __init__(self, inputs, tokenized_inputs, labels):
        #self.split = split
        self.inputs = inputs
        self.tokenized_inputs = tokenized_inputs
        self.labels = [label + 1 for label in labels]
        
        self.max_input_len = 50
        # Input sequence length = [CLS] + input + [SEP]
        self.max_seq_len = 1 + self.max_input_len + 1
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        inputs = self.inputs[idx]
        tokenized_inputs = self.tokenized_inputs[idx]
        label = self.labels[idx]
        # Add special tokens (101: CLS, 102: SEP)
        input_ids = [101] + tokenized_inputs.ids[:self.max_input_len] + [102]
        input_ids, token_type_ids, attention_mask = self.padding(input_ids)
        return torch.tensor(input_ids), torch.tensor(token_type_ids), torch.tensor(attention_mask), torch.tensor(label)

    def padding(self,input_ids):
        # Pad zeros if sequence length is shorter than max_seq_len
        padding_len = self.max_seq_len - len(input_ids)
        
        token_type_ids = [1] * len(input_ids) + [0] * padding_len
        attention_mask = [1] * len(input_ids) + [0] * padding_len
        input_ids = input_ids + [0] * padding_len
        return input_ids, token_type_ids, attention_mask

