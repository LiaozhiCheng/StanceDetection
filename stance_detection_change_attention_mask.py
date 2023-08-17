# -*- coding: utf-8 -*-
import json
import torch
from tqdm import tqdm

import math
from torch import default_generator, randperm
from torch._utils import _accumulate
from torch.utils.data.dataset import Subset
from transformers import BertTokenizer, BertForSequenceClassification, BertTokenizerFast
from torch.utils.data import DataLoader, Dataset

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Chinese news dataset
def read_data(file):
    with open(file, 'r', encoding="utf-8") as reader:
        datas = json.load(reader)

        return [data['title'] for data in datas], [data['body'] for data in datas], [data['summarize'] for data in datas], [int(data['stance']) for data in datas], [int(data['sentiment']) for data in datas], [data['target_token'] for data in datas]

data_title, data_body, data_summarize, data_stance, data_sentiment, data_target_token = read_data('news_stance_token_dataset_v2.json')

# Load the pre-trained BERT model and tokenizer
tokenizer = BertTokenizerFast.from_pretrained("bert-base-chinese")
model = BertForSequenceClassification.from_pretrained('ckiplab/bert-base-chinese', num_labels=3).to(device)
labels = {'negative': -1, 'neutral': 0, 'positive':1}

#Tokenize data
data_title_tokenized = tokenizer(data_title, add_special_tokens = False)

class StanceDataset(Dataset):
    def __init__(self, inputs, tokenized_inputs, target_token, labels):
        #self.split = split
        self.inputs = inputs
        self.tokenized_inputs = tokenized_inputs
        self.labels = [label + 1 for label in labels]
        self.target_words = target_token
        self.target_index = list()
        self.target_position = list()
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

        target_index = self.get_target_index()
        for i in target_index:
           input_ids[target_index+1] *= 1

        input_ids, token_type_ids, attention_mask = self.padding(input_ids)
        
        return torch.tensor(input_ids), torch.tensor(token_type_ids), torch.tensor(attention_mask), torch.tensor(label)
    def get_target_index(self):
        target_index = []
        text = self.inputs
        target_token = self.target_index
        for item in target_token:
           index = text.find(item)
           target_index.extend([i for i in range(index,index+len(item))])
        target_index = list(set(target_index))
        return target_index
    def padding(self,input_ids):
        # Pad zeros if sequence length is shorter than max_seq_len
        padding_len = self.max_seq_len - len(input_ids)
        
        token_type_ids = [1] * len(input_ids) + [0] * padding_len
        attention_mask = [1] * len(input_ids) + [0] * padding_len
        # target_index = self.get_target_index()
        # for i in target_index:
        #    attention_mask[target_index+1] = 1
        input_ids = input_ids + [0] * padding_len
        return input_ids, token_type_ids, attention_mask


stance_dataset = StanceDataset(data_title, data_title_tokenized, data_target_token, data_stance)

train_batch_size = 5

#train_loader = DataLoader(stance_dataset, batch_size=train_batch_size, shuffle=True, pin_memory=True)

"""###Split train and test data"""

def random_split(dataset, lengths,
                 generator=default_generator):
    r"""
    Randomly split a dataset into non-overlapping new datasets of given lengths.

    If a list of fractions that sum up to 1 is given,
    the lengths will be computed automatically as
    floor(frac * len(dataset)) for each fraction provided.

    After computing the lengths, if there are any remainders, 1 count will be
    distributed in round-robin fashion to the lengths
    until there are no remainders left.

    Optionally fix the generator for reproducible results, e.g.:

    >>> random_split(range(10), [3, 7], generator=torch.Generator().manual_seed(42))
    >>> random_split(range(30), [0.3, 0.3, 0.4], generator=torch.Generator(
    ...   ).manual_seed(42))

    Args:
        dataset (Dataset): Dataset to be split
        lengths (sequence): lengths or fractions of splits to be produced
        generator (Generator): Generator used for the random permutation.
    """
    if math.isclose(sum(lengths), 1) and sum(lengths) <= 1:
        subset_lengths: List[int] = []
        for i, frac in enumerate(lengths):
            if frac < 0 or frac > 1:
                raise ValueError(f"Fraction at index {i} is not between 0 and 1")
            n_items_in_split = int(
                math.floor(len(dataset) * frac)  # type: ignore[arg-type]
            )
            subset_lengths.append(n_items_in_split)
        remainder = len(dataset) - sum(subset_lengths)  # type: ignore[arg-type]
        # add 1 to all the lengths in round-robin fashion until the remainder is 0
        for i in range(remainder):
            idx_to_add_at = i % len(subset_lengths)
            subset_lengths[idx_to_add_at] += 1
        lengths = subset_lengths
        for i, length in enumerate(lengths):
            if length == 0:
                warnings.warn(f"Length of split at index {i} is 0. "
                              f"This might result in an empty dataset.")

    # Cannot verify that dataset is Sized
    if sum(lengths) != len(dataset):    # type: ignore[arg-type]
        raise ValueError("Sum of input lengths does not equal the length of the input dataset!")

    indices = randperm(sum(lengths), generator=generator).tolist()  # type: ignore[call-overload]
    return [Subset(dataset, indices[offset - length : offset]) for offset, length in zip(_accumulate(lengths), lengths)]

train_dataset, test_dataset = random_split(stance_dataset, [0.8, 0.2])
train_loader = DataLoader(train_dataset, batch_size=train_batch_size, shuffle=True, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True, pin_memory=True)


num_epoch = 5
validation = False
learning_rate = 1e-4
logging_step = 100
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
model.train()
def accuracy(list1, list2):
  right = 0
  for i in range(len(list1)):
    if list1[i] == list2[i]: 
      right+=1
  return (right/len(list1))
label_list = list()
print('Start Training ...')
for epoch in range(num_epoch):
    step = 1
    train_loss = train_acc = 0
    for batch in tqdm(train_loader):
      #print(batch)
      # Load all data into GPU
      batch = [i.to(device) for i in batch]

      # Model outputs: loss, logits
      output = model(input_ids=batch[0],token_type_ids=batch[1], attention_mask=batch[2], labels = batch[3])
      predict_label = torch.argmax(output.logits, dim=1)

      train_acc += accuracy(predict_label, batch[3])
      train_loss += output.loss

      output.loss.backward()
      optimizer.step()
      optimizer.zero_grad()
      step+=1

      learning_rate /= step
      optimizer.param_groups[0]["lr"] -= learning_rate

      if step % logging_step == 0:
        print(f"Epoch {epoch + 1} | Step {step} | loss = {train_loss.item() / logging_step:.3f}, acc = {train_acc / logging_step:.3f}")
        train_loss = train_acc = 0



model.train()
print("Saving Model ...")
model_save_dir = "saved_model" 
model.save_pretrained(model_save_dir)

print(accuracy(predict_label, batch[3]))

model.eval()
acc_time = 0
result = []
with torch.no_grad():
  for batch in test_loader:
    output = model(input_ids = batch[0].to(device), token_type_ids = batch[1].to(device), attention_mask = batch[2].to(device))
    predict_label = torch.argmax(output.logits, dim=1)
    # print(batch[3])
    if int(predict_label[0]) == int(batch[3]):
      acc_time+=1
    
print(acc_time/len(test_dataset))

model.eval()
support_acc_time, neutral_acc_time, against_acc_time = 0,0,0
support_label_time, neutral_label_time, against_label_time = 0,0,0
result = []
with torch.no_grad():
  for batch in test_loader:
    output = model(input_ids = batch[0].to(device), token_type_ids = batch[1].to(device), attention_mask = batch[2].to(device))
    predict_label = torch.argmax(output.logits, dim=1)
    if int(predict_label[0]) == int(batch[3]) and int(batch[3]) == 0:
      support_acc_time+=1
    if int(batch[3]) == 0:
      support_label_time += 1
    if int(predict_label[0]) == int(batch[3]) and int(batch[3]) == 1:
      neutral_acc_time+=1
    if int(batch[3]) == 1:
      neutral_label_time += 1
    if int(predict_label[0]) == int(batch[3]) and int(batch[3]) == 2:
      against_acc_time+=1
    if int(batch[3]) == 2:
      against_label_time += 1
print('support',support_acc_time/support_label_time)
print('neutral',neutral_acc_time/neutral_label_time)
print('against',against_acc_time/against_label_time)
