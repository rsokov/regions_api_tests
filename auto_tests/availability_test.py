import json
from urllib import request

test_url = 'https://regions-test.2gis.com/1.0/regions'
status_code = 200
response_type = 'application/json; charset=utf-8'
total = 'total'
items = 'items'
items_id = 'id'
items_name = 'name'
items_code = 'code'
items_country = 'country'
items_country_name = 'name'
items_country_code = 'code'

# Проверка доступности сервиса.
# Если сервис отдает HTTP-код 200 - тест считается пройденным.
# При любом другом ответе - тест фейлится.
def test_2gis_regions_api_availability():
    data = request.urlopen(test_url)
    assert data.code == status_code

# Проверка, что формат ответа в виде json
# Если формат ответа JSON в кодировке UTF8 - тест пройден
# Если формат ответа отличается от JSON в кодировке UTF8 - тест провален
def test_2gis_regions_api_response_type_json():
    data = request.urlopen(test_url)
    assert data.headers['Content-Type'] == response_type

# Проверка структуры ответа API на наличие полей, описанных документацией
# Тест считается пройденным, если все поля, описанные документацией и тестом присутствуют в ответе API
# Тест провален, если нет хотя бы одного из полей
def test_2gis_regions_api_response_structure():
    data = request.urlopen(test_url)
    json_data = json.loads(data.read().decode('utf-8'))
    assert total in json_data
    assert items in json_data
    assert items_id in json_data[items][0]
    assert items_name in json_data[items][0]
    assert items_code in json_data[items][0]
    assert items_country in json_data[items][0]
    assert items_country_name in json_data[items][0][items_country]
    assert items_country_code in json_data[items][0][items_country]


