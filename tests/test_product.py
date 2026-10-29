import pytest
from src.product import Product, Smartphone, LawnGrass

def test_product_creation():
    p = Product("Чай", "Чёрный", 100.0, 5)
    assert p.name == "Чай"
    assert p.description == "Чёрный"
    assert p.price == 100.0
    assert p.quantity == 5


def test_product_default_description():
    p = Product("Кофе", price=200.0, quantity=3)
    assert p.description == "без комментариев"


def test_product_zero_quantity_raises():
    with pytest.raises(ValueError):
        Product("Чай", quantity=0)


def test_product_negative_quantity_raises():
    with pytest.raises(ValueError):
        Product("Чай", quantity=-1)


def test_product_new_product_factory():
    data = {
        "name": "Кофе",
        "description": "Арабика",
        "price": 250.0,
        "quantity": 10,
    }
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Кофе"
    assert p.description == "Арабика"
    assert p.price == 250.0
    assert p.quantity == 10


def test_product_new_product_zero_quantity_raises():
    data = {
        "name": "Чай",
        "description": "",
        "price": 100.0,
        "quantity": 0,
    }
    with pytest.raises(ValueError):
        Product.new_product(data)


def test_product_price_property_setter_invalid():
    p = Product("Чай", price=100.0, quantity=5)
    old_price = p.price
    p.price = -10  # вызовет print, но мы его не проверяем
    assert p.price == old_price  # цена не должна обновиться на отрицательную


def test_product_price_property_setter_valid():
    p = Product("Чай", price=100.0, quantity=5)
    p.price = 150.0
    assert p.price == 150.0


def test_product_add_returns_total_cost():
    p1 = Product("Чай", price=100.0, quantity=2)
    p2 = Product("Кофе", price=250.0, quantity=1)
    total = p1 + p2
    assert total == (100.0 * 2) + (250.0 * 1)  # 450.0


def test_product_add_different_type_raises():
    p = Product("Чай", price=100.0, quantity=2)
    with pytest.raises(TypeError):
        _ = p + "string"


def test_smartphone_creation():
    s = Smartphone(
        name="iPhone",
        description="Смартфон",
        price=80000.0,
        quantity=3,
        efficiency=9.5,
        model="14 Pro",
        memory=256,
        color="серый",
    )
    assert s.name == "iPhone"
    assert s.price == 80000.0
    assert s.quantity == 3
    assert s.efficiency == 9.5
    assert s.model == "14 Pro"
    assert s.memory == 256
    assert s.color == "серый"


def test_smartphone_inheritance_from_product():
    s = Smartphone("Phone", price=50000.0, quantity=1)
    with pytest.raises(ValueError):
        Smartphone("Phone", quantity=0)


def test_lawn_grass_creation():
    g = LawnGrass(
        name="Газонная трава",
        description="Универсальная",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="зелёный",
    )
    assert g.name == "Газонная трава"
    assert g.price == 500.0
    assert g.quantity == 20
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"
    assert g.color == "зелёный"


def test_lawn_grass_inheritance_from_product():
    g = LawnGrass("Трава", price=300.0, quantity=10)
    with pytest.raises(ValueError):
        LawnGrass("Трава", quantity=0)
