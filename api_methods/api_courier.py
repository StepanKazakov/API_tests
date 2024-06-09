import requests


class ApiService:
    base_url = "https://qa-scooter.praktikum-services.ru/api/v1"

    @staticmethod
    def login_courier(login, password):
        payload = {
            "login": login,
            "password": password
        }
        return requests.post(f"{ApiService.base_url}/courier/login", json=payload)

    @staticmethod
    def create_order(order_data):
        return requests.post(f"{ApiService.base_url}/orders", json=order_data)

    @staticmethod
    def get_orders():
        return requests.get(f"{ApiService.base_url}/orders")

    @staticmethod
    def delete_courier(courier_id):
        return requests.delete(f"{ApiService.base_url}/courier/{courier_id}")
