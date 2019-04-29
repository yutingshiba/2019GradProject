import json
from elasticsearch import Elasticsearch


def post_request(req):
    """

    :param req:
    :return:
    """
    if not req:
        return "ERR: Request is empty"
    return insert_indexes(req)


def insert_indexes(req):
    """

    :param req:
    :return:
    """
    try:
        data = json.loads(req.form.get('data', '[]'))
        if not data or not data.get('d_list'):
            return "Post failed with data: {}".format(data)
        index = data.get('index', 'patient-temperature-test')
        doc_type = 'patient_temperature'
        count = 0
        d_list = data.get('d_list', [])
    except Exception as e:
        return "Caught exception {}; {}".format(type(e), str(e))

    es = Elasticsearch(
        ['es-cn-45912d6qn0008bb67.public.elasticsearch.aliyuncs.com'],
        http_auth=('elastic', 'MDR_test'),
        port=9200,
        use_ssl=False
    )
    for body in d_list:
        es.index(index=index, doc_type=doc_type, body=body)
        count += 1
    return "Post {} data".format(count)


def test():
    return "post_utils"
