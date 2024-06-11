import allure

from api_methods.api_courier import ApiCourier
from conftest import *


@allure.feature('Проверки методов курьера')
class TestCourier:
    @classmethod   # Используем @classmethod setup_class для создания экземпляра ApiCourier один раз для всего класса.
    def setup_class(cls):
        cls.courier = ApiCourier()

    @allure.title('Создание нового курьера со всеми заполненными полями (логин, пароль и имя)')
    def test_create_new_courier(self, full_courier_data):
        with allure.step(f'Создаем курьера со сгенерированными данными: {full_courier_data}'):
            response = self.courier.create_courier(full_courier_data)
        with allure.step('Проверяем статус-код ответа == 201 и что в ответе получено "ok": True'):
            assert response.status_code == 201
            assert response.json().get("ok") is True

    @allure.title('Создание нового курьера с заполненными только обязательными полями (логин и пароль)')
    def test_create_new_courier(self, required_courier_data):
        with allure.step(f'Создаем курьера со сгенерированными данными: {required_courier_data}'):
            response = self.courier.create_courier(required_courier_data)
        with allure.step('Проверяем статус-код ответа == 201 и что в ответе получено "ok": True'):
            assert response.status_code == 201
            assert response.json().get("ok") is True

    @allure.title('Создание курьера с уже существующим логином')
    def test_create_double_courier(self, full_courier_data):
        with allure.step(f'Создаем курьера: {full_courier_data}'):
            self.courier.create_courier(full_courier_data)
        with allure.step('Пытаемся создать курьера с тем же логином, но с другим именем и паролем'):
            courier_password = generate_random_string(10)
            courier_name = generate_random_string(10)
            duplicate_login = {
                "login": full_courier_data["login"],
                "password": courier_password,
                "first_name": courier_name
            }
            response = self.courier.create_courier(duplicate_login)
        with allure.step('Проверяем статус-код ответа == 409'):
            assert response.status_code == 409

    @allure.title('Создание курьера без пароля только с именем и логином')
    def test_create_courier_without_password(self):
        with allure.step(f'Пытаемся создать курьера без пароля со сгенерированным логином (пароль - пустая строка)'):
            courier_login = generate_random_string(10)
            courier_name = generate_random_string(10)
            courier_data = {"login": courier_login, "first_name": courier_name}
            response = self.courier.create_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 400'):
            assert response.status_code == 400

    @allure.title('Создание курьера без логина только с именем и паролем')
    def test_create_courier_without_login(self):
        with allure.step(f'Пытаемся создать курьера без логина со сгенерированными именем и паролем'):
            courier_password = generate_random_string(10)
            courier_name = generate_random_string(10)
            courier_data = {"first_name": courier_name, "password": courier_password}
            response = self.courier.create_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 400'):
            assert response.status_code == 400

    @allure.title('Проверка логина нового курьера')
    def test_login_courier(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step('Логинимся курьером с теми же данными'):
            response = self.courier.login_courier(required_courier_data)
        with allure.step('Проверяем статус-код ответа == 200 и наличие id в теле ответа'):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title('Запрос логина курьера без пароля')
    def test_login_courier_without_password(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step(f'Пытаемся залогиниться без ввода пароля'):
            courier_data = {"login": required_courier_data["login"], "password": ''}
            response = self.courier.login_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 400'):
            assert response.status_code == 400

    @allure.title('Запрос логина курьера без логина')
    def test_login_courier_without_login(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step(f'Пытаемся залогиниться с паролем без логина'):
            courier_data = {"password": required_courier_data["password"]}
            response = self.courier.login_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 400'):
            assert response.status_code == 400

    @allure.title('Запрос логина курьера с несуществующими логином и паролем')
    def test_login_unregistered_courier(self, required_courier_data):
        with allure.step(f'Пытаемся залогиниться несуществующим курьером: {required_courier_data}'):
            response = self.courier.login_courier(required_courier_data)
        with allure.step('Проверяем статус-код ответа == 404'):
            assert response.status_code == 404

    @allure.title('Запрос логина курьера с неправильным паролем')
    def test_login_courier_with_wrong_password(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step('Пытаемся залогиниться с новым сгенерированным паролем и со старым логином'):
            courier_password = generate_random_string(10)
            courier_data = {"login": required_courier_data["login"], "password": courier_password}
            response = self.courier.login_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 404'):
            assert response.status_code == 404

    @allure.title('Запрос логина курьера с неправильным логином')
    def test_login_courier_with_wrong_password(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step('Пытаемся залогиниться с новым сгенерированным логином и со старым паролем'):
            courier_login = generate_random_string(10)
            courier_data = {"password": required_courier_data["password"], "login": courier_login}
            response = self.courier.login_courier(courier_data)
        with allure.step('Проверяем статус-код ответа == 404'):
            assert response.status_code == 404

    @allure.title('Создаем и удаляем курьера')
    def test_create_and_delete_courier(self, required_courier_data):
        with allure.step(f'Создаем курьера: {required_courier_data}'):
            self.courier.create_courier(required_courier_data)
        with allure.step('Логинимся курьером и сохраняем его id'):
            login_response = self.courier.login_courier(required_courier_data)
            courier_id = login_response.json().get("id")
        with allure.step('Удаляем созданного курьера по id'):
            delete_response = self.courier.delete_courier(courier_id)
        with allure.step('Проверяем статус-код ответа == 200 и что в ответе получено "ok": True'):
            assert delete_response.status_code == 200
            assert delete_response.json().get("ok") is True

    @allure.title('Запрос на удаление курьера без указания id')
    def test_delete_courier_without_id(self):
        with allure.step('Пытаемся удалить курьера без указания id'):
            delete_response = self.courier.delete_courier(None)
        with allure.step('Проверяем статус-код ответа == 500 '
                         '(здесь баг - при отсутствии id должен быть статус-код 400)'):
            assert delete_response.status_code == 500

    @allure.title('Запрос на удаление курьера с указанием несуществующего id')
    def test_delete_courier_with_fake_id(self):
        with allure.step('Пытаемся удалить курьера с несуществующим id'):
            delete_response = self.courier.delete_courier(999999999)
        with allure.step('Проверяем статус-код ответа == 404'):
            assert delete_response.status_code == 404
