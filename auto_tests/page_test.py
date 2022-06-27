import json
from urllib import request, parse

test_url = 'https://regions-test.2gis.com/1.0/regions?'
page_param = 'page='
default_page_num = 1
test_incorrect_page_int_numbers = [-1, 0]
test_incorrect_page_symbols = ['qq', '1@', '!!', 'first', '-1.3', 'в']
total = 'total'
items = 'items'
items_id = 'id'

# Получение количества страниц в ответе API
def get_pages_count():
    data = request.urlopen(test_url + page_param + str(default_page_num))
    json_data = json.loads(data.read().decode('utf-8'))
    pages_count = 1 + json_data[total] // len(json_data[items])
    return pages_count


# Этот тест проверяет, что при отсутствии параметра page применяется значение по умолчанию (1) и
# выводятся объекты с 1ой страницы выдачи.
# Тест пройден, если объекты в ответе на запрос без параметра page соответствуют объектам с page=1
# Тест не пройден, если объекты в ответе на запрос без параметра page НЕ соответствуют объектам с page=1
def test_2gis_regions_api_page_default_value():
    page_data = request.urlopen(test_url + page_param + str(default_page_num))
    json_page_data = json.loads(page_data.read().decode('utf-8'))

    default_data = request.urlopen(test_url)
    json_default_data = json.loads(default_data.read().decode('utf-8'))

    assert sorted(json_default_data.items()) == sorted(json_page_data.items())


# Этот тест проверяет, что при указании параметра page в пределах допустимых значений
# API отдает данные, а не какую-либо ошибку
def test_2gis_regions_api_page_correct_values():
    pages_count = get_pages_count()
    for i in range(1, pages_count + 1):
        data = request.urlopen(test_url + page_param + str(i))
        json_data = json.loads(data.read().decode('utf-8'))
        assert len(json_data[items]) >= 0


# Проверка работы валидации, предупреждающей о том, что параметр page должен быть больше 0
# Тест пройден если при значениях <=0 (меньше или равно 0) выдается сообщение валидации
# Тест не пройден, если выводится что-либо, отличное от сообщения валидации
def test_2gis_regions_api_page_incorrect_int_numbers():
    error_message = "Параметр 'page' должен быть больше 0"
    for i in range(len(test_incorrect_page_int_numbers)):
        data = request.urlopen(test_url + page_param + str(test_incorrect_page_int_numbers[i]))
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == error_message


# Проверка работы валидации, предупреждающей о том, что параметр page должен быть целым числом
# Тест пройден, если при значениях параметра page не являющихся целым числом, выдается сообщение валидации
# Тест не пройден, если выводится что-либо, отличное от сообщения валидации
#
# NOTE: В этом тесте исправлена опечатка в тексте ошибки.
# # Пока эта опечатка не будет исправлена на стороне API - тест будет фейлиться при любых входных данных
def test_2gis_regions_api_page_incorrect_symbols():
    error_message = "Параметр 'page' должен быть целым числом"
    for i in range(len(test_incorrect_page_symbols)):
        page_num = parse.quote(test_incorrect_page_symbols[i])
        data = request.urlopen(test_url + page_param + page_num)
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == error_message
