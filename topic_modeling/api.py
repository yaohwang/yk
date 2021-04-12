# encoding: utf-8

import os
import sys
import traceback

from flask                    import Blueprint
from flask                    import request
from .classify_comment_taptap import predict


topic_bp = Blueprint('topic', __name__)


def check_params(params):
    pass


def parse_params(params):
    # TODO:
    return (params['texts'], )


def parse_result(params, result):
    # TODO:
    r = {}
    r['topics'] = result
    if params.get('texts_sendback', 1): r['texts'] = params['texts']
    return r


def callback(status, message, result):
    return {
               'status' : status,
               'message': message,
               'result' : result
           }


@topic_bp.route('/nlp/v1/topic/slg/taptap', methods=['POST'])
def detect_ads():
    status  = 0
    message = ''
    result  = {}

    try:
        # get params
        # print(request.json)
        """
        {
            "texts" : ['测试', ...],
            "texts_sendback" : 1,
        }
        """
        params = request.get_json()
        check_params(params)

        # predict
        result = parse_result(params, predict(*parse_params(params)))
        # callback
        return callback(status, message, result)

    except:
        # callback
        status  = 1
        message = traceback.format_exc()
        print(message)
        return callback(status, '', result)
