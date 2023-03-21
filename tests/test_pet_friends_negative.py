from api import PetFriends
from settings import *


pf = PetFriends()

def test_get_api_key_for_invalid_user(email=invalid_email_1, password=invalid_password_1):
    """ Проверяем, что запрос api ключа возвращает статус 403, если email невалидный, password невалидный"""

    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user_1(email=valid_email, password=invalid_password_1):
    """ Проверяем, что запрос api ключа возвращает статус 403, если email валидный, password невалидный"""

    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_invalid_filter(filter='abc'):
    """ Проверяем, что запрос всех питомцев возвращает ошибку 500 при невалидном filter"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает ошибку 403 при невалидном auth_key."""

    auth_key = {'key': 'e1590ca9d09fb05b807f863c3890a5e7eda363f7'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_add_new_pet_with_invalid_data_without_photo(name='Тишка', animal_type='кот', age='-4'):
    """Проверяем, что нельзя добавить питомца с некорректными данными (ошибка 400): age - отрицательное число
    (1-ый метод в Swagger)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400

def test_failed_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем отсутствие возможности обновления информации о питомце методом patch (код
    ошибки 405"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info_with_invalid_method(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    else:
        pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        status, result = pf.update_pet_info_with_invalid_method(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 405


def test_failed_update_pet_photo(pet_photo='images/Cat.gif'):
    """Проверяем отсутствие возможности добавления фото питомца в неправильном формате (gif)"""
    # Полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 403
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")