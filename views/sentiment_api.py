from flask import Blueprint, jsonify, request

from models import sentiment_index, access_data, sentiment_analysis


sentiment_api = Blueprint('sentiment_api', __name__)

#輸入媒體，輸出此家媒體的sentiment_index
@sentiment_api.route('media_sentiment_index', methods=['GET'])
def Media_sentiment_index_cal():
    media = request.values.get('media')
    if media == '':
        return jsonify({'message': '未輸入媒體'})
    
    news_list = access_data.Get_news(from_name=media)
    if news_list == []:
        return jsonify({'message': '資料集無此媒體'})

    senti_index = sentiment_index.Sentiment_index(news_list)
    media_dict = dict()
    media_dict['media'] = media
    media_dict['sentiment_index'] = senti_index
    return jsonify(media_dict)


#輸入類別，輸出此類別所有媒體的sentiment_index
@sentiment_api.route('categ_sentiment_index_list', methods=['GET'])
def Categ_sentiment_index_list():

    category = request.values.get('categ')
    print(category)
    if category == '':
        return jsonify({'message': '未輸入類別'})
    
    news_list = access_data.Get_news(page_category=category)
    if news_list == []:
        return jsonify({'code':'5000200','category': category, 'message': '資料集無此類別'})

    media_news_dict = access_data.Sort_news_by_media(news_list) #key: media / value: news_list
    media_sentiment_index_list = list()

    for media in media_news_dict:
        senti_index = sentiment_index.Sentiment_index(media_news_dict[media])
        media_sentiment_index_list.append({'News_media': media,'sentiment_index': senti_index})

    return jsonify(media_sentiment_index_list)

#輸入(相關資訊) 得sentiemt_analysis point list
@sentiment_api.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis_func():
    # Get the input data
    if request.is_json:
        data = request.get_json()
        input_title = data.get('title', None)
        predict_label = sentiment_analysis.single_prediction(input_title)
        output_dict  = dict()
        output_dict['title'] = input_title
        output_dict['sentiment_prediction'] = predict_label
        result = jsonify(output_dict)
    else:
        result = 'Not Json Data'
    # Return the predictions as JSON
    return result


