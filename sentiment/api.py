# encoding: utf-8

import os
import sys
import traceback

from pathlib import Path
from flask import Blueprint
from flask import request
from fasttext.FastText import load_model

from .service import predict


sentiment_bp = Blueprint('sentiment', __name__)

path_current = Path(__file__).parent
name_model = 'sentiment-20210909-1.mdl'
path_model = path_current/'model'/name_model
model = load_model(path_model)


def parse_params(params):
    return (model, params['texts'])


def parse_result(params, result):
    r = {}
    r['sentiments'] = result
    if params.get('texts_sendback', 1): r['texts'] = params['texts']
    return r


def callback(status, message, result):
    return {
               'status' : status,
               'message': message,
               'result' : result
           }


@sentiment_bp.route('/nlp/v1/sentiment', methods=['POST'])
def sentiment():
    status  = 0
    message = ''
    result  = {}

    try:
        """
        {
            "texts" : ['测试', ...],
            "texts_sendback" : 1,
        }
        """
        params = request.get_json()

        result = parse_result(params, predict(*parse_params(params)))
        return callback(status, message, result)

    except:
        # callback
        status  = 1
        message = traceback.format_exc()
        print(message)
        return callback(status, '', result)
