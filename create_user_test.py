import sender_stand_request
import data


def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body


# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201

    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе 
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1


# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")


def negative_assert_symbol(first_name):
    # Генерируем тело запроса с негативным именем пользователя
    user_body = get_user_body(first_name)

    # Отправляем запрос и получаем ответ
    response = sender_stand_request.post_new_user(user_body)

    # Проверяем, что код ответа 400
    assert response.status_code == 400

    # Проверяем, что в теле ответа атрибут code 400
    assert response.json()["code"] == 400

    # Проверяем мессадж
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские " \
                                         "или латинские буквы, длина должна быть не менее 2 и не более 15 символов"


# Тест 3. Неуспешное создание пользователя
# firstName 1 символ
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")


# Тест 4. Неуспешное создание пользователя
# firstName 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")


# Тест 5. Успешное создание пользователя
# firstName из букв латиницы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


# Тест 6. Успешное создание пользоватеоя
# firstName из букв кириллицы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


# Тест 7. Негативная проверка
# Пробелы в имени
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")


# Тест 8. Негативная проверка
# Спецсимволы в имени
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol('№%@')


# Тест 9. Негативная проверка
# Цифры в имени
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


def negative_assert_no_first_name(user_body):
    # cохраняем ответ
    response = sender_stand_request.post_new_user(user_body)

    # проверяем, что код ответа 400
    assert response.status_code == 400

    # проверяем, что атрибут кода в теле ответа тоже 400
    assert response.json()["code"] == 400

    # проверяем мессадж
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 10. Негативная проверка
# Нет параметра
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop('firstName')
    negative_assert_no_first_name(user_body)


# Тест 11. Негативная проверка
# Пустой параметр
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body('')
    negative_assert_no_first_name(user_body)


# Тест 10. Негативная проверка
# Нет параметра
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400


test_create_user_2_letter_in_first_name_get_success_response()
test_create_user_15_letter_in_first_name_get_success_response()
test_create_user_1_letter_in_first_name_get_error_response()
test_create_user_16_letter_in_first_name_get_error_response()
test_create_user_english_letter_in_first_name_get_success_response()
test_create_user_russian_letter_in_first_name_get_success_response()
test_create_user_has_space_in_first_name_get_error_response()
test_create_user_has_special_symbol_in_first_name_get_error_response()
test_create_user_has_number_in_first_name_get_error_response()
test_create_user_no_first_name_get_error_response()
test_create_user_empty_first_name_get_error_response()
test_create_user_number_type_first_name_get_error_response()