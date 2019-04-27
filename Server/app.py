"""
Author: yutinglin
environment: PyCharm
py_version: 3.6
date: 2019/04/18
"""

from flask import Flask
from flask import request
from elasticsearch import Elasticsearch
import json

from clientAPI import post_utils
from clientAPI import get_utils


app = Flask(__name__)


@app.route('/clients', methods=['GET', 'POST'])
def listen_to_request():
    if request.method == 'GET':
        return get_utils.get_request(request)
    elif request.method == 'POST':
        return post_utils.post_request()
    return 'Request type should be either GET or POST; got {} instead'.format(request.method)


def request_info(name, timestamp):
    if not name or not timestamp:
        return "Failed"


    print("\n\n--- Request sent ---\n\n")
    total = resp.get('hits', {}).get('total', -1)
    print()
    print("\n\n--- Content printed ---\n\n")
    return json.dumps(resp.get('hits', {}).get('hits', [])[:10], indent=4)


if __name__ == '__main__':
    post_utils.test()

    #app.run(debug=True, port=8874)
    #app.run(debug=True, host='211.75.30.99', port=8874)
