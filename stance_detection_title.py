# -*- coding: utf-8 -*-
import json
import torch
from tqdm import tqdm
from transformers import BertTokenizer, BertForSequenceClassification, BertTokenizerFast
from torch.utils.data import DataLoader, Dataset
import argparse
## Get Data
def get_parser():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('--file', default='news_stance_dataset.json')
    parser.add_argument('--pretrain_sentiment', default=0)
    return parser
parser = get_parser()
args = parser.parse_args()

data_file = args.file
is_pretrain_sentiment = args.pretrain_sentiment
print("Data file:" + data_file)


device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Chinese news dataset
def read_data(file):
    with open(file, 'r', encoding="utf-8") as reader:
        datas = json.load(reader)

        return [data['title'] for data in datas], [data['body'] for data in datas], [data['summarize'] for data in datas], [int(data['stance']) for data in datas], [int(data['sentiment']) for data in datas]

train_title, train_body, train_summarize, train_stance, train_sentiment = read_data(data_file)

# Load the pre-trained BERT model and tokenizer
tokenizer = BertTokenizerFast.from_pretrained("bert-base-chinese")
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=3).to(device)
labels = {'negative': -1, 'neutral': 0, 'positive':1}

if is_pretrain_sentiment != 0:
  model_path = "sentiment_model/pytorch_model.bin"
  state_dict = torch.load(model_path)
  model.load_state_dict(state_dict)


#Tokenize data
train_title_tokenized = tokenizer(train_title, add_special_tokens = False)

max_num = 0
for title in train_title:
  if len(title) > max_num:
    max_num = len(title)
print(max_num)

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


stance_dataset = StanceDataset(train_title, train_title_tokenized, train_stance)

train_batch_size = 4

train_loader = DataLoader(stance_dataset, batch_size=train_batch_size, shuffle=True, pin_memory=True)

num_epoch = 2
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

print("Saving Model ...")
model_save_dir = "stance_model" 
model.save_pretrained(model_save_dir)
