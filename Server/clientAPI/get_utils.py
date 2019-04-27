import json
import time
from elasticsearch import Elasticsearch

def get_request(req):
    """

    :param req:
    :return:
    """
    if not req:
        return "Request empty"
    name = req.args.get('name', '')
    mint = int(req.args.get('mintimestamp', -1))
    limit_n = int(req.args.get('limit', 20))
    if not name:
        return "Name is required"
    elif limit_n > 20 or limit_n <= 0:
        return "limit should be between 1 - 20"

    latency = 20
    mint = int(time.time() - latency) * 1000 if mint < 0 else mint

    resp = get_user_info_from_es(name, mint, limit_n)
    return resp if resp else "ES request failed"


def get_user_info_from_es(name, mint, limit_n):
    """

    :param name:
    :param mint:
    :param limit_n:
    :return:
    """

    es = Elasticsearch(
        ['es-cn-45912d6qn0008bb67.public.elasticsearch.aliyuncs.com'],
        http_auth=('elastic', 'MDR_test'),
        port=9200,
        use_ssl=False
    )
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

    resp = es.search(index="patient-temperature-test", body=body)
    return sorted(resp, key=sort_hits, reverse=True) if resp else None


def sort_hits(x):
    """
    
    :param x: 
    :return: 
    """
    return x.get('_source', {}).get('timestamp', -1)
