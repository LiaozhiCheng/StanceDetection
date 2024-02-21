#計算各家媒體的stance狀況
from pymongo import MongoClient
import math 
DB = MongoClient('mongodb://localhost:27017')['Media_data']
NEWS_COLLECTION = DB['news_raw']

media_stance = dict()
for i in NEWS_COLLECTION.find({"stance": {"$in":["1","0","-1"]}}):
    if i['source'] not in media_stance:
        media_stance[i['source']] = {"implicit_sentiment" :{"positive":0, "negative":0, "neutral":0}, 'stance':{"positive":0, "negative":0, "neutral":0}}

    if i["implicit_sentiment"] == 1:
        media_stance[i['source']]["implicit_sentiment"]['positive'] += 1
    elif i["implicit_sentiment"] == -1:
        media_stance[i['source']]["implicit_sentiment"]['negative'] += 1
    else :
        media_stance[i['source']]["implicit_sentiment"]['neutral'] += 1
    try:
        if i["stance"] == "1":
            media_stance[i['source']]['stance']['positive'] += 1
        elif i["stance"] == "-1":
            media_stance[i['source']]['stance']['negative'] += 1

        else :
            media_stance[i['source']]['stance']['neutral'] += 1
    except:
        print(i)

for media, stance_index in media_stance.items():
    num_report = stance_index['stance']['positive'] +stance_index['stance']['negative'] +stance_index['stance']['neutral']
    if num_report < 50:
        continue
    print(media,num_report)
    #by other thesis

    print("stance: ",math.log((stance_index['stance']['positive']+1)/(stance_index['stance']['negative']+1)))
    print("implicit_sentiment: ", math.log((stance_index["implicit_sentiment"]['positive']+1)/(stance_index["implicit_sentiment"]['negative']+1)))
    #my contribution

    #print(stance_index)