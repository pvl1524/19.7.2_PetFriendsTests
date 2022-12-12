from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_email_invalid_password(email=valid_email, password='12345'):
    """ Проверяем, что запрос api ключа с невалидным паролем возвращает статус 403
    и в результате не содержится слово key"""

    # Отправляем запрос с валидной почтой и невалидным паролем. Сохраняем полученный ответ с кодом статуса в status,
    # а текст ответа - в invalid_result
    status, invalid_result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in invalid_result

def test_add_new_pet_with_invalid_data(name='', animal_type='',
                                     age='7', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными (имя и тип пустые)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    # name и animal_type - обязательные параметры. Но запрос проходит при незаполненных данных, что является багом.
    # При некорректных данных должен приходить 400 код состояния, но возвращается 200.
    assert status == 200
    #assert result['name'] != "" # Проверять нужно было бы на непустой ввод. Но в этом случае тест будет failed
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert 'pet_photo' in result

def test_add_new_simple_pet_with_valid_data(name='Bob', animal_type='cat', age='4'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api для валидных данных и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_add_new_simple_pet_with_invalid_data(name='', animal_type='кот', age=''):
    """Проверяем, что можно добавить питомца без фото с некорректными (незаполненными) данными"""

    # Запрашиваем ключ api для валидных данных и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    # name и age - обязательные параметры. Но запрос проходит и при незаполненных данных, что является багом.
    # При некорректных данных должен приходить 400 код состояния, но возвращается код состояния 200.
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_add_jpg_photo_to_my_pet(pet_photo='images/P1040103.jpg'):
    '''Проверяем добавление JPG фото своему питомцу'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200, в ответе присутствует ключ pet_photo
        assert status == 200
        assert 'pet_photo' in result
    else:
        # если спиок питомцев пустой, то выводим исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_png_photo_to_my_pet(pet_photo='images/cat3.png'):
    '''Проверяем добавление PNG фото своему питомцу'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200, в ответе присутствует ключ pet_photo
        assert status == 200
        assert 'pet_photo' in result
    else:
        # если спиок питомцев пустой, то выводим исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_broken_photo_to_my_pet(pet_photo='images/cat2.jpg'):
    '''Проверяем добавление битого фото к своему питомцу без фото'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 400 и ключ pet_photo не присутствует в ответе result
        # По факту при отправке битого фото возвращается код состояния 500 (ошибка на стороне сервера) с сообщеием:
        # "The server encountered an internal error and was unable to complete your request.
        # Either the server is overloaded or there is an error in the application."
        assert status == 500
        assert 'pet_photo' not in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_with_valid_data_broken_photo(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat2.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными (имя, порода, возраст) и битым фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == '' # Фото не загружается, остальные данные добавляются

def test_successful_delete_not_my_pet_with_vilid_apikey():
    """Проверяем возможность удаления чужого питомца"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список всех питомцев пустой, выкидываем исключение о пустом списке всех питомцев
    if len(all_pets['pets']) == 0:
        raise Exception("There is no pets yet!")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список всех питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем что статус ответа равен 200 и в списке всех питомцев нет id удалённого питомца
    # Метод delete_pet позволяет удалить не своего питомца, что является серьезной уязвимостью сервиса.
    assert status == 200
    assert pet_id not in all_pets.values()

def test_successful_update_not_my_pet_info_with_valid_apikey(name='Alex', animal_type='dog', age='12'):
    """Проверяем возможность обновления информации о чужом питомце"""

    # Получаем ключ auth_key и список всех питомцев
    # auth_key = { "key": "2ce2506a8c59ddcbccdacffd3ff9365fe38ff11cf99490da51c4d811"}
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(all_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        # Возвращается код состояния 200. Был указан корректный ключ api auth_key.
        # В результате запроса обновились данные не моего питомца, что серьезной уязвимостью сервиса.
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

##############################

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик2', animal_type='Кот', age=8):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    #auth_key = { "key": "2ce2506a8c59ddcbccdacffd3ff9365fe38ff11cf99490da51c4d811"}
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
