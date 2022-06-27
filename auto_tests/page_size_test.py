import json
from urllib import request, parse

test_url = 'https://regions-test.2gis.com/1.0/regions?'
page_size_param = 'page_size='
default_page_size = 15
available_page_size = [5, 10, 15]
test_correct_page_size = available_page_size
test_incorrect_page_size_numbers = [0, -1, 20]
test_incorrect_page_size_symbols = ['qq', '1@', '150"']
items = 'items'


# Проверка корректности выдачи если page_size не задан (по умолчанию должно выводиться 15 записей на страницу)
# Если в ответе API отображается количество элементов на странице определенных default_page_size- тест пройден
# При любом другом количестве элементов на странице - тест фейлится.
def test_2gis_regions_api_page_size_default():
    data = request.urlopen(test_url)
    json_data = json.loads(data.read().decode('utf-8'))
    assert len(json_data[items]) == default_page_size


# Проверка количества записей на странице при page_size равному одному из допустимых значений (available_page_size)
# Если в ответе API кол-во элементов на странице совпадает с заданным page_size - тест пройден
# Если в ответе API кол-во элементов на странице НЕ совпадает с заданным page_size - тест провален
def test_2gis_regions_api_page_size_correct():
    for i in range(len(test_correct_page_size)):
        data = request.urlopen(test_url + page_size_param + str(test_correct_page_size[i]))
        json_data = json.loads(data.read().decode('utf-8'))
        assert len(json_data[items]) == test_correct_page_size[i]


# Проверка работы валидации при page_size вне диапазона допустимых значений
# Если в ответе API возвращается ошибка "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15" - тест пройден
# При любом другом ответе API - тест провален
def test_2gis_regions_api_page_size_incorrect_numbers():
    error_message = "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15"
    for i in range(len(test_incorrect_page_size_numbers)):
        data = request.urlopen(test_url + page_size_param + str(test_incorrect_page_size_numbers[i]))
        json_data = json.loads(data.read().decode('utf-8'))

        assert json_data['error']['message'] == error_message


# Проверка работы валидации при page_size с недопустимым форматом значений
# Если в ответе API возвращается ошибка "Параметр 'page_size' должен быть целым числом" - тест пройден
# При любом другом ответе API - тест провален
#
# NOTE: В этом тесте исправлена опечатка в тексте ошибки.
# Пока эта опечатка не будет исправлена на стороне API - тест будет фейлиться при любых входных данных
def test_2gis_regions_api_page_size_incorrect_symbols():
    error_message = "Параметр 'page_size' должен быть целым числом"
    for i in range(len(test_incorrect_page_size_symbols)):
        page_size_num = parse.quote(test_incorrect_page_size_symbols[i])
        data = request.urlopen(test_url + page_size_param + page_size_num)
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == error_message
