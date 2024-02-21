#計算各家媒體的stance狀況
from pymongo import MongoClient
import math 
DB = MongoClient('mongodb://localhost:27017')['Media_data']
NEWS_COLLECTION = DB['news_raw']

media_stance = dict()
for i in NEWS_COLLECTION.find({"stance": {"$in":["1","0","-1"]}}):
    if i['source'] not in media_stance:
        media_stance[i['source']] = {"positive":0, "negative":0, "neutral":0}

    if i["stance"] == "1":
        media_stance[i['source']]['positive'] += 1
    elif i["stance"] == "-1":
        media_stance[i['source']]['negative'] += 1

    else :
        media_stance[i['source']]['neutral'] += 1

for media, stance_index in media_stance.items():
    print(media)
    #by other thesis
    print(math.log((stance_index['positive']+1)/(stance_index['negative']+1)))
    #my contribution

    print(stance_index)