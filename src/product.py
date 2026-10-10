class Product:
    name: str
    description: str
    price: float
    quantity: int


    def __init__(self, name, description='без комментариев', price=0, quantity=0):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity


    def __str__(self):
        return f'{self.name}, {self.__price} руб. Остаток: {self.quantity} шт.'


    def __add__(self, other):
        return (self.__price * self.quantity) + (other.__price * other.quantity)


    @classmethod
    def new_product(cls, prod_wok):
        name = prod_wok['name']
        description = prod_wok['description']
        price = prod_wok['price']
        quantity = prod_wok['quantity']
        return cls(name, description, price, quantity)


    # Геттер получения цены
    @property
    def price(self):
        return self.__price


    # Сеттер установки цены
    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value
