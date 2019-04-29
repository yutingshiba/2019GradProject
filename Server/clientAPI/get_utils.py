import json
from elasticsearch import Elasticsearch
import env


def get_request(req, is_single):
    """

    :param req:
    :param is_single: if it's a single get request
    :return:
    """
    try:
        if not req:
            return "ERR: Request is empty"
        return get_single_req(req) if is_single else get_multi_req(req)
    except Exception as e:
        return "get request caught exception: {}\n{}".format(type(e), str(e))


def get_single_req(req):
    """

    :param req:
    :return:
    """
    name = req.args.get('name', '')
    timestamp = int(req.args.get('timestamp', -1))
    if not name or timestamp < 0:
        para_format = {
            'name': 'user_name',
            'timestamp': 'timestamp (second)'
        }
        return "Usage: should include parameters {}".format(json.dumps(para_format))

    resp = get_user_info_from_es(name, timestamp)
    return resp if resp else "ES request failed"


def get_multi_req(req):
    """

    :param req:
    :return:
    """
    name = req.args.get('name', '')
    mint = int(req.args.get('mintimestamp', -1))
    maxt = int(req.args.get('maxtimestamp', -1))
    if not name or mint < 0 or maxt < 0:
        para_format = {
            'name': 'user_name',
            'mintimestamp': 'minimum timestamp (second)',
            'maxtimestamp': 'maximum timestamp (second)',
        }
        return "Usage: should include parameters {}".format(json.dumps(para_format))
    n = maxt - mint + 1
    if n < 2 or n > 600:
        return "Usage: 0 < maxtimestamp - mintimestamp < 600"

    resp = get_user_info_from_es(name, mint, n)
    return resp if resp else "ES request failed"


def get_user_info_from_es(name, mint, limit_n=1):
    """

    :param name:
    :param mint:
    :param limit_n:
    :return:
    """
    # sec to millisec
    mint *= 1000

    body = {
        "query": {
            "bool": {
                "must": {"match": {"name": name}},
                "filter": {
                    "range": {
                        "timestamp": {
                            "gte": mint,
                            "lt": mint + limit_n * 1000
                        }
                    }
                }
            }
        }
    }

    es = Elasticsearch(
        env.es_hosts,
        port=9200,
        use_ssl=False
    )
    resp = es.search(index=env.es_index, body=body)
    return json.dumps(sorted(resp.get('hits', {}).get('hits', []),
                             key=sort_hits, reverse=True) if resp else None)


def sort_hits(x):
    """
    
    :param x: 
    :return: 
    """
    return x.get('_source', {}).get('timestamp', -1)
