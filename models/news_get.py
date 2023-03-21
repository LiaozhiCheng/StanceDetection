from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from models import _db


def test_models_fuc():
    return 'I am handsome.'

def get_news_info(news_title):
    data = _db.NEWS_COLLECTION.find_one({'title':news_title}) #不能直接return會有bson問題
    if data:
        print(data)
        return {'title': data['title'], 'url': data['url'], 'body': data['body']}
    else:
        return dict()