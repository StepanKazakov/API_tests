from base_methods import BaseMethods


class ApiCourier(BaseMethods):
    def __init__(self):
        super().__init__()

    def create_courier(self, payload):
        return self.post("/courier", payload)

    def login_courier(self, payload):
        return self.post("/courier/login", payload)

    def delete_courier(self, courier_id):
        return self.delete("/courier", object_id=courier_id)
