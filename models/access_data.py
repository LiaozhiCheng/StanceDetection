from models._db import FB_COLLECTION


def Get_news(**kwargs):
    #media --> news_list
    return [news for news in FB_COLLECTION.find(kwargs)]

def Get_media(**kwargs):
    media_set = {news['from_name'] for news in FB_COLLECTION.find(kwargs)}
    return list(media_set)

def Sort_news_by_media(news_list):
    #key:media value:news
    media_news_dict = dict()
    for news in news_list:
        if news['from_name'] not in media_news_dict:
            media_news_dict[news['from_name']] = [news]
        else:
            media_news_dict[news['from_name']].append(news)
    return media_news_dict
    
    