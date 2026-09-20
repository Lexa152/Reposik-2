import pytest

from src.product import Product
from src.category import Category


@pytest.fixture
def prod1():
    return Product(
        name='Банан кормовой',
        description='корм скотине',
        price=10.5,
        quantity=500
        )


@pytest.fixture
def prod2():
    return Product(
        name='Банан человеческий',
        description='для человека',
        price=100.3,
        quantity=100
        )


@pytest.fixture
def prod3():
    return Product(
        name='Банан экзотический',
        description='которые не от мира сего - для них',
        price=900000.0,
        quantity=3
        )


@pytest.fixture
def prod4():
    return Product(
        name='Картофель',
        description='нормальный овощ',
        price=5.0,
        quantity=100000000
        )


@pytest.fixture
def cat1():
    return Category(
        name='Фрукты',
        description='продукты, богатые клетчаткой и витаминами',
        products=[prod1, prod2, prod3],
        )


@pytest.fixture
def cat2():
    return Category(
        name='Овощи',
        description='питательные, полезные овощи',
        products=[prod4],
        )


@pytest.fixture
def cat3():
    return Category(
        name='Съедобные продукты',
        description='питательные, полезные овощи',
        products=[prod1, prod2, prod3, prod4],
        )
