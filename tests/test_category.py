import pytest
from src.category import Category
from src.product import Product

def test_init_empty_products_list():
    """пустой список продуктов """
    cat = Category("Электроника", "Всё для дома", [])
    assert cat.name == "Электроника"
    assert cat.description == "Всё для дома"
    assert cat.product_count == 0
    assert cat.products.strip() == ""


def test_init_with_products_list():
    """передача списка продуктов """
    p1 = Product("Ноутбук", "Игровой", 99999.0, 3)
    p2 = Product("Мышь", "Беспроводная", 1499.0, 20)
    cat = Category("Компьютеры", "Техника для работы", [p1, p2])

    assert cat.name == "Компьютеры"
    assert cat.product_count == 2
    assert "Ноутбук" in cat.products
    assert "Мышь" in cat.products


def test_init_none_products():
    """products=None """
    cat = Category("Книги", "Художественная литература", None)
    assert cat.product_count == 0
    assert cat.products.strip() == ""


def test_products_list_is_copied_not_referenced():
    """список продуктов копируется """
    external_list = [Product("Товар", "Тест", 100.0, 5)]
    cat = Category("Тестовая", "Описание", external_list)

    external_list.clear()

    assert cat.product_count == 1
    assert "Товар" in cat.products


def test_add_product_increases_count_and_updates_products():
    """add_product """
    p = Product("Наушники", "С шумоподавлением", 5990.0, 10)
    cat = Category("Аудио", "Звук и музыка", [])

    cat.add_product(p)

    assert cat.product_count == 1
    assert "Наушники" in cat.products
    assert "5990.0 руб." in cat.products
    assert "шт." in cat.products


def test_add_multiple_products():
    """add_product добавление нескольких продуктов """
    p1 = Product("Клавиатура", "Механическая", 7990.0, 5)
    p2 = Product("Веб-камера", "HD", 2490.0, 8)
    cat = Category("Аксессуары", "Дополнения к ПК", [])

    cat.add_product(p1)
    cat.add_product(p2)

    assert cat.product_count == 2
    assert "Клавиатура" in cat.products
    assert "Веб-камера" in cat.products


def test_products_property_format_per_line():
    """Проверка формата строки products """
    p1 = Product("Монитор", "27 дюймов", 25000.0, 4)
    p2 = Product("SSD", "1 ТБ", 8000.0, 15)
    cat = Category("Комплектующие", "Для ПК", [p1, p2])

    lines = cat.products.strip().split("\n")
    assert len(lines) == 2

    for line in lines:
        assert "руб." in line
        assert "шт." in line

    # оба товара присутствуют
    assert any("Монитор" in l for l in lines)
    assert any("SSD" in l for l in lines)


def test_category_count_increments_on_each_init():
    """category_count увеличивается на 1 """
    initial_count = Category.category_count

    Category("Категория 1", "Описание 1", [])
    Category("Категория 2", "Описание 2", [])
    Category("Категория 3", "Описание 3", [])

    assert Category.category_count == initial_count + 3


def test_product_count_does_not_share_between_instances():
    """product_count """
    cat1 = Category("Категория A", "Описание A", [Product("A1", "", 10.0, 1)])
    cat2 = Category("Категория B", "Описание B", [])

    assert cat1.product_count == 1
    assert cat2.product_count == 0

    cat2.add_product(Product("B1", "", 20.0, 1))
    assert cat1.product_count == 1  # не изменился
    assert cat2.product_count == 1


def test_adding_duplicate_product_allowed():
    """Дубликаты продуктов """
    p = Product("Товар", "Дубликат", 100.0, 1)
    cat = Category("Дубликаты", "Разрешены", [])

    cat.add_product(p)
    cat.add_product(p)  # добавляем тот же объект

    assert cat.product_count == 2
    # В строке products две одинаковые строки
    assert cat.products.count("Товар") == 2

