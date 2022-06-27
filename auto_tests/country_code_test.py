import json
from urllib import request, parse


test_url = 'https://regions-test.2gis.com/1.0/regions?'
country_code_param = 'country_code='
page_param = 'page='
page_size_param = 'page_size='
default_page_num = 1
total = 'total'
items = 'items'
items_country = 'country'
items_country_code = 'code'

incorrect_country_codes_list = ['ка', 'gb', 'usa', '11', '@@', '..', ' ', '']


# Получение количества страниц в ответе API
def get_pages_count():
    data = request.urlopen(test_url + page_param + str(default_page_num))
    json_data = json.loads(data.read().decode('utf-8'))
    pages_count = 1 + json_data[total] // len(json_data[items])
    return pages_count


# Проверка корректности вывода списка регионов с country_code='ru'.
# В ответе API должны быть только регионы с country_code = 'ru'.
# При наличии в ответе региона с другим country_code тест пофейлится.
def test_2gis_regions_api_country_code_ru():
    country_code = 'ru'
    for i in range(1, get_pages_count() + 1):
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        for i in range(len(json_data[items])):
            assert json_data[items][i][items_country][items_country_code] == country_code


# Проверка корректности вывода списка регионов с country_code='kz'.
# В ответе API должны быть только регионы с country_code = 'kz'.
# При наличии в ответе региона с другим country_code тест пофейлится.
def test_2gis_regions_api_country_code_kz():
    country_code = 'kz'
    for i in range(1, get_pages_count() + 1):
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        for i in range(len(json_data[items])):
            assert json_data[items][i][items_country][items_country_code] == country_code


# Проверка корректности вывода списка регионов с country_code='kg'.
# В ответе API должны быть только регионы с country_code = 'kg'.
# При наличии в ответе региона с другим country_code тест пофейлится.
def test_2gis_regions_api_country_code_kg():
    country_code = 'kg'
    for i in range(1, get_pages_count() + 1):
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        for i in range(len(json_data[items])):
            assert json_data[items][i][items_country][items_country_code] == country_code


# Проверка корректности вывода списка регионов с country_code='cz'.
# В ответе API должны быть только регионы с country_code = 'cz'.
# При наличии в ответе региона с другим country_code тест пофейлится.
def test_2gis_regions_api_country_code_cz():
    country_code = 'cz'
    for i in range(1, get_pages_count() + 1):
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        for i in range(len(json_data[items])):
            assert json_data[items][i][items_country][items_country_code] == country_code


# Проверка валидации поля country_code с значением 'ua'.
# Тест сделан для наглядности. Думаю его можно объединить с test_2gis_regions_api_country_code_another_values
# Тест считается пройденным, если в ответе API возвращается ошибка
# Тест не пройден, если возвращается ответ, отличный от сообщения об ошибке
def test_2gis_regions_api_country_code_ua():
    country_code = 'ua'
    message = "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz"
    for i in range(1, get_pages_count() + 1):
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == message


# Проверка валидации поля country_code при различных заведомо некорректных значениях
# Тест считается пройденным, если в ответе API возвращается ошибка
# Тест не пройден, если возвращается любой ответ, отличный от сообщения об ошибке
def test_2gis_regions_api_country_code_another_values():
    message = "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz"
    for i in range(len(incorrect_country_codes_list)):
        country_code = parse.quote(incorrect_country_codes_list[i])
        data = request.urlopen(test_url + country_code_param + country_code + '&' + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == message
