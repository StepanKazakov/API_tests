import allure

from base_methods import BaseMethods


class ApiCourier(BaseMethods):
    def __init__(self):
        super().__init__()

    @allure.step('Создание курьера')
    def create_courier(self, payload):
        return self.post("/courier", payload)

    @allure.step('Логин курьера')
    def login_courier(self, payload):
        return self.post("/courier/login", payload)

    @allure.step('Удаление курьера')
    def delete_courier(self, courier_id):
        return self.delete("/courier", object_id=courier_id)
