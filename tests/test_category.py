import pytest
from src.category import Category

# класс Product
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

    @classmethod
    def new_product(cls, prod_wok):
        name = prod_wok['name']
        description = prod_wok['description']
        price = prod_wok['price']
        quantity = prod_wok['quantity']
        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


# Класс Category
class Category:
    name: str
    description: str
    products = list
    product_count: int = 0
    category_count: int = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        if products is None:
            self.__products = []
        else:
            self.__products = list(products)
        self.product_count += len(self.__products)
        Category.category_count += 1

    def add_product(self, prod):
        self.__products.append(prod)
        self.product_count += 1
        Category.product_count += 1

    @property
    def products(self):
        product_str = ''
        for prod in self.__products:
            product_str += f'{prod.name}, {prod.price:.2f} руб. Остаток: {prod.quantity} шт. \n'
        return product_str


# Тесты
def test_category_init_empty():
    category = Category("Электроника", "Товары для дома", [])
    assert category.name == "Электроника"
    assert category.description == "Товары для дома"
    assert category.product_count == 0
    assert Category.category_count == 1


def test_category_init_none():
    category = Category("Одежда", "Стильная одежда", None)
    assert category.products == ""
    assert category.product_count == 0


def test_category_init_with_products():
    prod1 = Product("Наушники", "Хорошие наушники", 5000, 10)
    prod2 = Product("Клавиатура", "Механическая клавиатура", 3000, 5)
    category = Category("Гаджеты", "Мелкая электроника", [prod1, prod2])

    assert category.name == "Гаджеты"
    assert category.product_count == 2
    assert "Наушники, 5000.00 руб." in category.products
    assert "Клавиатура, 3000.00 руб." in category.products


def test_add_product():
    category = Category("Книги", "Художественная литература", [])
    book = Product("Война и мир", "Классика", 800, 3)
    category.add_product(book)
    assert category.product_count == 1
    assert "Война и мир, 800.00 руб." in category.products


def test_add_multiple_products():
    category = Category("Игрушки", "Для детей", [])
    toy1 = Product("Машинка", "Быстрая машинка", 500, 20)
    toy2 = Product("Кукла", "Красивая кукла", 700, 15)
    category.add_product(toy1)
    category.add_product(toy2)
    assert category.product_count == 3
    assert "Машинка, 500.00 руб." in category.products
    assert "Кукла, 700.00 руб." in category.products


def test_products_property_format():
    prod = Product("Чайник", "Электрический чайник", 2500, 4)
    category = Category

