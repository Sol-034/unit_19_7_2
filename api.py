import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings import valid_mail, valid_password
import json


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> tuple:
        """Метод возвращает статус код и ключ авторизации"""
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url + 'api/key', headers=headers)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filter) -> tuple:
        """Метод возвращает статус код и список питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets',
                           headers=headers,
                           params=filter)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self,
                    auth_key: dict,
                    name: str,
                    animal_type: str,
                    age: str,
                    path_to_pet_photo: str) -> tuple:
        """Метод добавляет питомца с фотографией"""
        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (path_to_pet_photo,
                                  open(path_to_pet_photo, 'rb'), 'images/jpeg')
                    })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets',
                            headers=headers,
                            data=data)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self,
                          auth_key: dict,
                          name: str,
                          animal_type: str,
                          age: str) -> tuple:
        """Метод добавляет питомца без фотографии"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}

        res = requests.post(self.base_url + 'api/create_pet_simple',
                            headers=headers,
                            data=data)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self,
                         auth_key: dict,
                         my_pet: dict,
                         path_to_pet_photo: str) -> tuple:
        """Метод добавляет фото для питомца по его ID"""
        data = MultipartEncoder(
            fields={'pet_photo': (path_to_pet_photo,
                                  open(path_to_pet_photo, 'rb'), 'images/jpeg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        pet_id = my_pet['id']

        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}',
                            headers=headers,
                            data=data)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, my_pet: dict) -> int:
        """Удалить питомца по его ID"""
        headers = {'auth_key': auth_key['key']}
        pet_id = my_pet['id']

        res = requests.delete(self.base_url + f'api/pets/{pet_id}',
                              headers=headers)

        status = res.status_code

        return status

    def update_pet(self,
                   auth_key: dict,
                   my_pet: dict,
                   name: str,
                   animal_type: str,
                   age: str) -> tuple:
        """Обновить данные о питомце по его ID"""
        data = {'name': name,
                'animal_type': animal_type,
                'age': age}

        headers = {'auth_key': auth_key['key']}
        pet_id = my_pet['id']

        res = requests.put(self.base_url + f'api/pets/{pet_id}',
                           headers=headers,
                           data=data)

        status = res.status_code
        result = ''

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# pf = PetFriends()

# _, auth_key = pf.get_api_key(valid_mail, valid_password)
# print(auth_key)

# filter = ''

# status, all_pets = pf.get_list_of_pets(auth_key, filter)
# print(status)

# filter = 'my_pets'

# status_2, my_pets = pf.get_list_of_pets(auth_key, filter)
# print(status_2,type(my_pets),my_pets['pets'][0])

# name = 'Сервалушка'
# animal_type = 'Котеище'
# age = 25
# path_to_pet_photo = "tests/images/picture_001.jpg"

# _, pet = pf.add_new_pet(auth_key, 'Вася', 'Кот', 5, path_to_pet_photo)
# print(pet)

# _, pet_without_photo = pf.create_pet_simple(auth_key, name, animal_type, age)
# print(pet_without_photo)

# _, pet_with_photo = pf.add_photo_of_pet(auth_key, pet_without_photo, path_to_pet_photo)
# print(pet_with_photo)

# _, update_pet = pf.update_pet(auth_key,my_pets['pets'][0], name, animal_type, age)
# print(update_pet)

# status, result = pf.delete_pet(auth_key,my_pets['pets'][0])
# print(status, my_pets['pets'], result)
