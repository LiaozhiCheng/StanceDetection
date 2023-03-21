from models._db import FB_COLLECTION
import math

#計算post的positive sentiment
def Positive_sentiment(emotions: dict) -> int:    
    #PositiveSentiment = Wow + Likes + 2 · Love
    return int(emotions['cW']) + int(emotions['cL']) + int(emotions['cO'])*2

#計算post的negative sentiment
def Negative_sentiment(emotions: dict) -> int:
    #NegativeSentiment = Haha + Sad + 2 · Angry
    return int(emotions['cH']) + int(emotions['cD']) + int(emotions['cA'])*2


#計算各個社團的sentiment_index
def Sentiment_index(news_list: list) -> float:   
    
    total_positive_sentiment = 0
    total_negative_sentiment = 0
    for news in news_list:
        total_positive_sentiment += Positive_sentiment(news)
        total_negative_sentiment += Negative_sentiment(news)
        
    
    
    #Sentiment Index = ln(TotalPositiveSentiment / TotalNegativeSentiment)
    return math.log((total_positive_sentiment+1)/(total_negative_sentiment+1))


if __name__ == '__main__':
    test_data_list = [news for news in FB_COLLECTION.find({'from_name': '康健雜誌'})]
    # print(test_data)

    print(test_data_list[0]['from_name'], Sentiment_index(test_data_list))
