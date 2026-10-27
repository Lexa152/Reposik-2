from abc import ABC, abstractmethod


class BaseProduct(ABC):

    @classmethod
    @abstractmethod
    def new_product(cls, prod_wok):
        pass


class PrintMixin:
    def after_init(self):
        print(repr(self))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})'


class Product(BaseProduct, PrintMixin):
    name: str
    description: str
    price: float
    quantity: int


    def __init__(self, name, description='без комментариев', price=0, quantity=0):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        self.after_init()


    def __str__(self):
        return f'{self.name}, {self.__price} руб. Остаток: {self.quantity} шт.'


    def __add__(self, other):
        if type(other) is type(self):
            return (self.__price * self.quantity) + (other.__price * other.quantity)
        else:
            raise TypeError


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


class Smartphone(Product):
    efficiency: float  # производительность
    model: str  # модель
    memory: int  # объем встроенной памяти
    color: str  # цвет

    def __init__(self, name,
                 description='без комментариев',
                 price=0,
                 quantity=0,
                 efficiency=0,
                 model='null',
                 memory=0,
                 color='null'):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):  # «Трава газонная» (LawnGrass)
    country: str  # страна-производитель
    germination_period: str  # срок прорастания кол-во дней от посева
    color: str  # цвет

    def __init__(self, name,
                 description='без комментариев',
                 price=0,
                 quantity=0,
                 country='null',
                 germination_period='null',
                 color='null'):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
