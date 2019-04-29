# -*- coding: utf-8 -*-
# Author: yutinglin
# environment: PyCharm
# py_version: 3.6
# file_name: app.py
# create_time: 2019/04/18 10:43
##########################

from flask import Flask
from flask import request

from Server.clientAPI import post_utils
from Server.clientAPI import get_utils


app = Flask(__name__)


@app.route('/getSingle', methods=['GET'])
def listen_to_request_single():
    if request.method == 'GET':
        return get_utils.get_request(request, True)
    return 'Request type should be GET; got {} instead'.format(request.method)


@app.route('/getMulti', methods=['GET'])
def listen_to_request_multi():
    if request.method == 'GET':
        return get_utils.get_request(request, False)
    return 'Request type should be GET; got {} instead'.format(request.method)


@app.route('/post', methods=['POST'])
def post_request():
    if request.method == 'POST':
        return post_utils.post_request(request)
    return 'Request type should be POST; got {} instead'.format(request.method)


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)
