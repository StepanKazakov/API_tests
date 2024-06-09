from base_methods import BaseMethods


class ApiOrders(BaseMethods):
    def __init__(self):
        super().__init__()

    def get_orders_list(self):
        return self.get_data("/orders")

    def create_order(self, payload):
        return self.post("/orders", payload)

    def get_order_by_id(self, order_id):
        return self.get_data(f"/orders/track?t={order_id}")
