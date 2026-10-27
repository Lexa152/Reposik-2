import pytest
from src.product import Product, Smartphone, LawnGrass


def test_product_init_default_values():
    p = Product("Чай")
    assert p.name == "Чай"
    assert p.description == "без комментариев"
    assert p.price == 0
    assert p.quantity == 0


def test_product_init_with_all_args():
    p = Product("Кофе", "Арабика", 350.5, 10)
    assert p.name == "Кофе"
    assert p.description == "Арабика"
    assert p.price == 350.5
    assert p.quantity == 10


def test_product_str():
    p = Product("Чай", "Зелёный", 250, 5)
    result = str(p)
    assert "Чай" in result
    assert "250 руб." in result
    assert "Остаток: 5 шт." in result


def test_product_add():
    p1 = Product("Чай", quantity=2, price=100)
    p2 = Product("Кофе", quantity=3, price=200)
    total = p1 + p2
    assert total == 800


def test_product_add_wrong_type():
    p = Product("Чай", quantity=2, price=100)
    with pytest.raises(TypeError):
        _ = p + "строка"


def test_product_new_product_factory():
    data = {
        "name": "Какао",
        "description": "Порошок",
        "price": 400,
        "quantity": 3
    }
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Какао"
    assert p.price == 400
    assert p.quantity == 3


def test_product_price_setter_valid():
    p = Product("Чай", price=250)
    p.price = 300
    assert p.price == 300


def test_product_price_setter_invalid():
    p = Product("Чай", price=250)
    p.price = -10
    assert p.price == 250


def test_smartphone_init():
    s = Smartphone(
        name="Phone X",
        description="Флагман",
        price=99900,
        quantity=2,
        efficiency=95.5,
        model="X10",
        memory=256,
        color="чёрный"
    )
    assert s.name == "Phone X"
    assert s.price == 99900
    assert s.quantity == 2
    assert s.efficiency == 95.5
    assert s.model == "X10"
    assert s.memory == 256
    assert s.color == "чёрный"


def test_smartphone_is_instance_of_product():
    s = Smartphone("Phone X", price=99900)
    assert isinstance(s, Product)


def test_lawn_grass_init():
    g = LawnGrass(
        name="Газонная трава Премиум",
        description="Для солнечных участков",
        price=500,
        quantity=4,
        country="Россия",
        germination_period="7-10 дней",
        color="зелёный"
    )
    assert g.name == "Газонная трава Премиум"
    assert g.price == 500
    assert g.quantity == 4
    assert g.country == "Россия"
    assert g.germination_period == "7-10 дней"
    assert g.color == "зелёный"


def test_lawn_grass_is_instance_of_product():
    g = LawnGrass("Трава", price=500)
    assert isinstance(g, Product)


def test_print_mixin_repr_basic():
    """Проверяем, что __repr__ возвращает ожидаемую строку для Product."""
    p = Product("Чай", "Чёрный", 100.0, 5)
    expected = "Product(Чай, Чёрный, 100.0, 5)"
    assert repr(p) == expected


def test_print_mixin_repr_with_subclasses():
    """__repr__ должен корректно работать и для подклассов (Smartphone, LawnGrass)."""
    s = Smartphone(
        "iPhone", "Флагман", 90000, 2,
        efficiency=0.9, model="15", memory=256, color="чёрный"
    )
    l = LawnGrass(
        "Газон Люкс", "Для дачи", 500, 10,
        country="Россия", germination_period="7 дней", color="зелёный"
    )

    # Проверяем, что в repr есть имя класса и базовые поля
    assert "Smartphone" in repr(s)
    assert "iPhone" in repr(s)

    assert "LawnGrass" in repr(l)
    assert "Газон Люкс" in repr(l)
