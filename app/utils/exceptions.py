class ClientNotFound(Exception):
    def __init__(self, client_id):
        self.client_id = client_id
        super().__init__(f"Client with id {client_id} not found")


class ProductAlreadyRegistered(Exception):
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"Product {product_id} already registered as favorite")


class EmailAlreadyRegistered(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"E-mail {email} already registered")


class ProductNotFound(Exception):
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"Product with id {product_id} not found")


class UserNotFound(Exception):
    def __init__(self):
        super().__init__("User not found")


class UserEmailAlreadyRegistered(Exception):
    def __init__(self):
        super().__init__(f"E-mail already registered")
