from flask import Blueprint, jsonify, request

from models import summarization, access_data

summarization_api = Blueprint('summarization_api', __name__)

#輸入媒體，輸出此家媒體的sentiment_index
@summarization_api.route('summarize_label_data_db', methods=['GET'])
def Media_sentiment_index_cal():
    

