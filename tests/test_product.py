from src.product import Product


def test_init_default_values():
    """Проверка значений по умолчанию """
    p = Product("Товар")
    assert p.name == "Товар"
    assert p.description == "без комментариев"
    assert p.price == 0
    assert p.quantity == 0


def test_init_custom_values():
    """Проверка передачи всех параметров в конструкторе """
    p = Product("Кружка", "Керамическая", 299.99, 10)
    assert p.name == "Кружка"
    assert p.description == "Керамическая"
    assert p.price == 299.99
    assert p.quantity == 10


def test_new_product_factory():
    """Проверка new_product """
    data = {
        "name": "Футболка",
        "description": "Хлопковая",
        "price": 1499.0,
        "quantity": 5
    }
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Футболка"
    assert p.description == "Хлопковая"
    assert p.price == 1499.0
    assert p.quantity == 5


def test_price_getter():
    """Пров геттера price """
    p = Product("Чайник", "Электрический", 3500.0, 2)
    assert p.price == 3500.0


def test_price_setter_valid():
    """Пров установки цены через сеттер """
    p = Product("Ложка", "Серебряная", 0, 1)
    p.price = 150.5
    assert p.price == 150.5


def test_price_setter_invalid_zero():
    """Проверка попытки установить нулевую цену """
    p = Product("Вилка", "Стальная", 200.0, 3)
    initial_price = p.price
    p.price = 0
    assert p.price == initial_price


def test_price_setter_invalid_negative():
    """Проверка попытки установить отрицательную цену """
    p = Product("Тарелка", "Фарфоровая", 400.0, 7)
    initial_price = p.price
    p.price = -50
    assert p.price == initial_price

