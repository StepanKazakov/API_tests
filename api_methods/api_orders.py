import allure

from base_methods import BaseMethods


class ApiOrders(BaseMethods):
    def __init__(self):
        super().__init__()

    @allure.step('Получения списка всех заказов')
    def get_orders_list(self):
        return self.get_data("/orders")

    @allure.step('Создание заказа')
    def create_order(self, payload):
        return self.post("/orders", payload)

    @allure.step('Получения описания заказа по id')
    def get_order_by_id(self, order_id):
        return self.get_data(f"/orders/track?t={order_id}")
