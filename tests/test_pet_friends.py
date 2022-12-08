from api import PetFriends
from settings import *


class TestPets:
    def setup(self):
        self.pf = PetFriends()

    # ПОЗИТИВНЫЕ ТЕСТЫ
    def test_get_api_key_for_valid_user(self,
                                        email: str = valid_mail,
                                        password: str = valid_password):
        """Получаем ключ авторизации используя валидные данные"""
        status, auth_key = self.pf.get_api_key(email, password)

        assert status == 200
        assert 'key' in auth_key

    def test_get_list_pets_with_valid_key(self,
                                          filter: str = ''):
        """Получаем список всех питомцев используя валидный ключ авторизации"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)

        status, all_pets = self.pf.get_list_of_pets(auth_key, filter)

        assert status == 200
        assert len(all_pets['pets']) > 0

    def test_add_new_pet_with_valid_key(self,
                                        name='Serval',
                                        animal_type='Кот',
                                        age='5',
                                        path_to_pet_photo='tests/images/picture_001.jpg'):
        """Добавляем питомца с фото"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)

        status, pet = self.pf.add_new_pet(auth_key,
                                          name,
                                          animal_type,
                                          age,
                                          path_to_pet_photo)

        assert status == 200
        assert "pet_photo" in pet

    def test_create_pet_simple_for_valid_key(self,
                                             name='Serval',
                                             animal_type='Кот',
                                             age='5'):
        """Добавляем простого питомца по валидному ключу авторизации"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)

        status, pet = self.pf.create_pet_simple(auth_key,
                                                name,
                                                animal_type,
                                                age)

        assert status == 200
        assert "animal_type" in pet

    def test_add_photo_of_pet_for_valid_key(self,
                                            path_to_pet_photo='tests/images/picture_001.jpg'):
        """Добавляем фотографию для питомца по валидному ключу авторизаци"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        pet = my_pets['pets'][0]

        status, result = self.pf.add_photo_of_pet(auth_key, pet, path_to_pet_photo)

        assert status == 200
        assert "animal_type" in pet

    def test_update_pet_for_valid_user(self,
                                       name='Vasya',
                                       animal_type='Котик',
                                       age='15'):
        """Обновляем данные питомца принадлежащего валидированному пользователю"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        old_pet = my_pets['pets'][0]

        status, update_pet = self.pf.update_pet(auth_key,
                                                old_pet,
                                                name,
                                                animal_type,
                                                age)

        assert status == 200
        assert old_pet['name'] != update_pet['name']
        assert old_pet['animal_type'] != update_pet['animal_type']
        assert old_pet['age'] != update_pet['age']

    def test_delete_pet_for_valid_user(self):
        """Удаляем питомца пренадлежащего валидированному пользователю"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        pet_for_delete = my_pets['pets'][0]

        status = self.pf.delete_pet(auth_key,
                                    pet_for_delete)

        # Обновляем данные о питомцах пользователя, чтобы корректно сравнить результат
        _, update_my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        # Проверяем, что питомец отсутствует в БД сервера
        assert len(my_pets['pets']) != len(update_my_pets['pets'])

    # НЕГАТИВНЫЕ ТЕСТЫ
    def test_get_api_key_for_invalid_mail(self,
                                          email: str = invalid_mail,
                                          password: str = valid_password):
        """Пробуем получить ключ авторизации используя невалидную почту"""
        status, auth_key = self.pf.get_api_key(email, password)

        assert status == 403
        assert not('key' in auth_key)

    def test_get_api_key_for_invalid_password(self,
                                              email: str = valid_mail,
                                              password: str = invalid_password):
        """Пробуем получить ключ авторизации используя невалидный пароль"""
        status, auth_key = self.pf.get_api_key(email, password)

        assert status == 403
        assert not('key' in auth_key)

    def test_get_api_key_with_empty_fields(self,
                                           email: str = '',
                                           password: str = ''):
        """Пробуем получить ключ авторизации без почты и пароля"""
        status, auth_key = self.pf.get_api_key(email, password)

        assert status == 403
        assert not('key' in auth_key)

    def test_get_list_pets_with_invalid_key(self, filter: str = ''):
        """Пробуем получить список всех питомцев используя невалидный ключ авторизации"""
        status, all_pets = self.pf.get_list_of_pets(invalid_auth_key, filter)

        assert status == 403
        assert not('pets' in all_pets)

    def test_add_new_pet_with_invalid_key(self,
                                          name='Serval',
                                          animal_type='Кот',
                                          age='5',
                                          path_to_pet_photo='tests/images/picture_001.jpg'):
        """Попробуем добавить питомца с фото используя невалидный ключ авторизации"""
        status, pet = self.pf.add_new_pet(invalid_auth_key,
                                          name,
                                          animal_type,
                                          age,
                                          path_to_pet_photo)

        assert status == 403
        assert not("pet_photo" in pet)

    def test_create_pet_simple_for_invalid_key(self,
                                               name='Serval',
                                               animal_type='Кот',
                                               age='5'):
        """Попробуем добавить простого питомца по невалидному ключу авторизации"""
        status, pet = self.pf.create_pet_simple(invalid_auth_key,
                                                name,
                                                animal_type,
                                                age)

        assert status == 403
        assert not("animal_type" in pet)

    def test_create_pet_simple_with_empty_fields(self,
                                                 name='',
                                                 animal_type='',
                                                 age=''):
        """Попробуем добавить простого питомца без заполнения данных"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)

        status, pet = self.pf.create_pet_simple(auth_key,
                                                name,
                                                animal_type,
                                                age)

        # Тут выявлен баг - добавляется питомец с пустыми полями, нотя они обязательны к заполнению
        # но в чатах было сказано, что все тесты должны быть passed, а где баг - коммент оставить
        assert status == 200
        assert "animal_type" in pet


    def test_create_pet_simple_with_negative_age(self,
                                                 name='Serval',
                                                 animal_type='Кот',
                                                 age='-5'):
        """Попробуем добавить простого питомца без заполнения данных"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)

        status, pet = self.pf.create_pet_simple(auth_key,
                                                name,
                                                animal_type,
                                                age)

        # Тут выявлен баг - добавляется питомец с отрицательным возрастом, что противоречит здравому смыслу
        # но в чатах было сказано, что все тесты должны быть passed, а где баг - коммент оставить
        assert status == 200
        assert "animal_type" in pet

    def test_update_pet_for_invalid_key(self,
                                        name='Vasya',
                                        animal_type='Котик',
                                        age='15'):
        """Пробуем обновить данные питомца пользователя по невалидному ключу авторизации"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        old_pet = my_pets['pets'][0]

        status, update_pet = self.pf.update_pet(invalid_auth_key,
                                                old_pet,
                                                name,
                                                animal_type,
                                                age)

        assert status == 403
        assert not("animal_type" in update_pet)

    def test_delete_pet_for_invalid_key(self):
        """Пробуем удалить питомца пользователя по невалидному ключу авторизации"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        pet_for_delete = my_pets['pets'][0]

        status = self.pf.delete_pet(invalid_auth_key, pet_for_delete)

        # Обновляем данные о питомцах пользователя, чтобы корректно сравнить результат
        _, update_my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 403
        # Проверяем, что количество питомцев не поменялось
        assert len(my_pets['pets']) == len(update_my_pets['pets'])

    def test_delete_pet_for_alien_user(self):
        """Пробуем удалить питомца не пренадлежащего пользователю"""
        _, auth_key = self.pf.get_api_key(valid_mail, valid_password)
        _, all_pets = self.pf.get_list_of_pets(auth_key, '')

        pet_for_delete = all_pets['pets'][0]

        status = self.pf.delete_pet(auth_key, pet_for_delete)

        # Обновляем данные о всех питомцах, чтобы корректно сравнить результат
        _, update_all_pets = self.pf.get_list_of_pets(auth_key, '')

        # Тут выявлен баг - удаляется чужой питомец
        # но в чатах было сказано, что все тесты должны быть passed, а где баг - коммент оставить
        assert status == 200
        # Проверяем, что количество питомцев не поменялось
        assert not(pet_for_delete in update_all_pets['pets'])
