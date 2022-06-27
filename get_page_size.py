import json
from urllib import request


def get_page_size():
    input_data = request.urlopen('https://regions-test.2gis.com/1.0/regions?page_size=15')
    data = json.loads(input_data.read().decode('utf-8'))
    page_size = len(data['items'])
    print(page_size)


get_page_size()
