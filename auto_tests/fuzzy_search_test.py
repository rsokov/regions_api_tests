import json
from urllib import request, parse

test_url = 'https://regions-test.2gis.com/1.0/regions?'
query_param = 'q='
items = 'items'

empty_search_value = ''
correct_search_values_list = ['орск', 'рск', 'москва', 'МосКвА', 'БИР', 'город', 'Петербург']
incorrect_search_values_list = ['ва', '11', 'd', ' ', '"']
not_found_values_list = ['вауу', 'арфыавы', '1111', 'qqqq', '@2"!!', '   ']

# Тест проверяет наличие сообщения валидации о том, что значение параметра q пустое
# Если при пустом значении q выводится сообщение об ошибке "Параметр 'q' не может иметь пустое значение" - тест пройден
# Если выводится что-либо другое, тест провален
def test_2gis_regions_api_fuzzy_search_empty_value():
    error_message = "Параметр 'q' не может иметь пустое значение"
    data = request.urlopen(test_url + query_param + empty_search_value)
    json_data = json.loads(data.read().decode('utf-8'))
    assert json_data['error']['message'] == error_message

# Тест проверяет правильность выдачи результатов при регистронезависимом поиске по вхождению в строку
# Тест получает ответ API и ищет вхождение подстроки в каждом элементе с названием города.
# Если каждый элемент содержит эту подстроку, тест пройден
# Если хотя бы один элемент НЕ содержит эту подстроку, тест провален
def test_2gis_regions_api_fuzzy_search_correct_value():
    for i in range(len(correct_search_values_list)):
        searching_query = parse.quote(correct_search_values_list[i])
        data = request.urlopen(test_url + query_param + searching_query)
        json_data = json.loads(data.read().decode('utf-8'))
        for j in json_data[items]:
            assert correct_search_values_list[i].lower() in j['name'].lower()

# Проверка валидации количества символов в поисковом запросе
# Если длина запроса менее 3 символов и выводится сообщение "Параметр 'q' должен быть не менее 3 символов" - тест пройден
# Иначе - тест провален
def test_2gis_regions_api_fuzzy_search_incorrect_value():
    error_message = "Параметр 'q' должен быть не менее 3 символов"
    for i in range(len(incorrect_search_values_list)):
        searching_query = parse.quote(incorrect_search_values_list[i])
        data = request.urlopen(test_url + query_param + searching_query)
        json_data = json.loads(data.read().decode('utf-8'))
        assert json_data['error']['message'] == error_message

# Проверка по заведомо несуществующим в БД значениям
# Если в ответе нет элементов-городов - тест пройден
# Иначе (есть города в выдаче или ошибка) - тест провален
def test_2gis_regions_api_fuzzy_search_not_found_value():
    for i in range(len(not_found_values_list)):
        searching_query = parse.quote(not_found_values_list[i])
        data = request.urlopen(test_url + query_param + searching_query)
        json_data = json.loads(data.read().decode('utf-8'))
        assert len(json_data[items]) == 0
