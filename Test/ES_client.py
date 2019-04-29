import time
import json
import random
import requests
from Server.clientAPI import env

from elasticsearch import Elasticsearch, RequestsHttpConnection


def create_doc(body, index=env.es_index, doc_type='_doc'):

    es = Elasticsearch(
        env.es_hosts,
        port=9200,
        use_ssl=False
    )

    res = es.index(index=index, doc_type=doc_type, body=body)
    return res['created']


def gen_patient(name, timestamp, period=10):
    """

    :param name:
    :param period: period of data to generate, unit is second
    :return:
    """
    if not name or not timestamp:
        print('ERR; no name or timestamp specified')
        return

    # temporary solution
    gender = {
        'Carl': 'male',
        'Coca': 'female',
        'Sprite': 'female',
        'Wachowski': 'male'
    }

    min_temp = 335
    max_temp = 390
    temperature = random.randint(340, 375)
    heart_rate = random.randint(60, 80)
    oxy = random.randint(940, 990)
    body_list = []
    for i in range(period):
        temperature = temperature + random.randint(-3, 3)
        temperature = max_temp if temperature > max_temp else temperature
        temperature = min_temp if temperature < min_temp else temperature

        body = {
            'name': name,
            'gender': gender.get(name, 'male'),
            'timestamp': (timestamp + i) * 1000,
            'heart_rate': heart_rate,
            'blood_oxygen': oxy / 10.,
            'temperature': temperature / 10.
        }
        body_list.append(body)
    #ipadd = '127.0.0.1'
    ipadd = '18.223.116.5'
    data = {'data': json.dumps({'d_list': body_list, 'index': 'patient_'})}
    resp = requests.post("http://{}/post".format(ipadd), data=data, timeout=10)
    #resp = requests.get("http://{}/getSingle".format(ipadd), timeout=4)
    print("Resp Status: {}".format(resp))
    print("Resp Content: {}".format(resp.content))
    #create_doc(body)


if __name__ == '__main__':
    period = 60
    cur_timestamp = int(time.time()) - period - 200
    for uname in ['Coca', 'Sprite', 'Wachowski']:
        print('Start create fake patient {}'.format(uname))
        gen_patient(uname, cur_timestamp, period=period)
