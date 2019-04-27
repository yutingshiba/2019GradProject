import time
import random

from elasticsearch import Elasticsearch, RequestsHttpConnection


def create_doc(body, index='patient-temperature-test', doc_type='patient_temperature'):

    es = Elasticsearch(
        ['es-cn-45912d6qn0008bb67.public.elasticsearch.aliyuncs.com'],
        http_auth=('elastic', 'MDR_test'),
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
    temperature = random.randint(340, 370)
    for i in range(period):
        temperature = temperature + random.randint(-3, 3)
        temperature = max_temp if temperature > max_temp else temperature
        temperature = min_temp if temperature < min_temp else temperature

        body = {
            'name': name,
            'gender': gender.get(name, 'male'),
            'timestamp': (timestamp + i) * 1000,
            'temperature': temperature / 10.
        }

        create_doc(body)


if __name__ == '__main__':
    period = 300
    timestamp = int(time.time()) - period - 200
    for name in ['Carl', 'Coca', 'Sprite', 'Wachowski']:
        print('Start create fake patient {}'.format(name))
        gen_patient(name, timestamp, period=period)
