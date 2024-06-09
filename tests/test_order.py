import allure
import pytest

from api_methods.api_orders import ApiOrders


@allure.feature('Проверки методов заказа')
class TestOrder:
    @classmethod   # Используем @classmethod setup_class для создания экземпляра ApiOrders один раз для всего класса.
    def setup_class(cls):
        cls.order = ApiOrders()

    @allure.title('Создание заказа')
    @pytest.mark.parametrize("color", [None, ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_create_order(self, color):
        with allure.step('Заполняем данные с параметризованным цветом и создаем заказ'):
            order_data = {
                            "firstName": "Ivan",
                            "lastName": "Petrovich",
                            "address": "Moscow",
                            "metroStation": 4,
                            "phone": "+7 800 355 35 35",
                            "rentTime": 5,
                            "deliveryDate": "2023-06-06",
                            "comment": "Test order",
                            "color": color
                        }
            response = self.order.create_order(order_data)
        with allure.step('Проверяем статус-код'):
            assert response.status_code == 201
        with allure.step('Проверяем что в теле ответа содержится номер заказа'):
            assert "track" in response.json()

    @allure.title('Получаем полный список заказов')
    def test_get_orders_list_full(self):
        with allure.step('Запрос списка заказов без параметров'):
            response = self.order.get_orders_list()
        with allure.step('Проверяем статус-код'):
            assert response.status_code == 200
        with allure.step('Проверяем что в теле ответа содержится список заказов'):
            response_json = response.json()
            assert isinstance(response_json["orders"], list)

    @allure.title('Запрос заказа по его номеру')
    def test_get_order_by_id(self):
        with allure.step('Заполняем данные и создаем заказ'):
            order_data = {
                "firstName": "Ivan",
                "lastName": "Petrovich",
                "address": "Moscow",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2023-06-06",
                "comment": "Test order",
                "color": ["GREY"]
            }
            response = self.order.create_order(order_data)
        with allure.step('Получаем номер заказа после его формирования и делаем запрос по номеру заказа'):
            order_id = response.json().get("track")
            order_response = self.order.get_order_by_id(order_id)
        with allure.step('Проверяем статус-код'):
            assert order_response.status_code == 200
        with allure.step('Проверяем что в теле ответа содержится объект с параметрами заказа'):
            response_json = order_response.json()
            assert isinstance(response_json["order"], object)

    @allure.title('Запрос заказа без номера')
    def test_get_order_without_id(self):
        with allure.step('Делаем запрос без указания номера заказа'):
            order_response = self.order.get_order_by_id(None)
        with allure.step('Проверяем статус-код'):
            assert order_response.status_code == 400

    @allure.title('Запрос заказа с несуществующим номером')
    def test_get_order_without_id(self):
        with allure.step('Делаем запрос с несуществующим номером заказа'):
            order_response = self.order.get_order_by_id(999999999)
        with allure.step('Проверяем статус-код'):
            assert order_response.status_code == 404
