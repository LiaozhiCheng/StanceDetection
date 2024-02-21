from pymongo import MongoClient
import math 
import json
from tqdm import tqdm
DB = MongoClient('mongodb://localhost:27017')['Media_data']
NEWS_COLLECTION = DB['news_raw']


with open('labeled_data_2.json', 'r', encoding = 'utf-8') as file:
    news_label_dataset = json.load(file)

for i in tqdm(news_label_dataset):
    NEWS_COLLECTION.update_many({'title':i['title']},{'$set':{'implicit_sentiment':i['implict_sentiment']}})
