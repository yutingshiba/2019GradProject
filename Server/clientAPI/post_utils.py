import json
from Server.app import es


def post_request(req):
    """

    :param req:
    :return:
    """
    if not req:
        return "ERR: Request is empty"
    resp = insert_indexes(req)
    if resp < 0:
        return "Post failed"
    return "Post {} data".format(resp)


def insert_indexes(req):
    """

    :param req:
    :return:
    """
    data = req.form.get('data', {})
    if not data or not data.get('d_list'):
        return -1
    index = data.get('index', 'patient-temperature-test')
    doc_type='patient_temperature'
    count = 0
    for d in data['d_list']:
        body = d
        es.index(index=index, doc_type=doc_type, body=body)
        count += 1
    return count


def test():
    return "post_utils"
