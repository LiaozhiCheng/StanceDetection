from flask import request, Blueprint, jsonify
from models import stance_detection


stance_api = Blueprint("stance_api", __name__)

@stance_api.route('/stance_detection', methods=['POST'])
def single_predict_api():
    # Get the input data
    if request.is_json:
        data = request.get_json()
        input_title = data.get('title', None)
        predict_label = stance_detection.single_prediction(input_title)
        output_dict  = dict()
        output_dict['title'] = input_title
        output_dict['stance_prediction'] = predict_label
        result = jsonify(output_dict)
    else:
        result = 'Not Json Data'
    # Return the predictions as JSON
    return result
