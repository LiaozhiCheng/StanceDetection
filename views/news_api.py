
from flask import request, Blueprint, jsonify
from models import news_get


news_api = Blueprint("news_api", __name__)

@news_api.route('/test')
def test():
    data = news_get.test_models_fuc() #string
    return data

@news_api.route('/get-news', methods = ['GET'])
def get_news():
    
    title = request.values.get('title')
    print(title)
    data = news_get.get_news_info(title) #dictionary
    return jsonify(data)