import pytest
from src.category import Category
from src.product import Product, Smartphone, LawnGrass


def test_category_init_with_empty_products():
    category = Category("Книги", "Художественная литература", [])
    assert category.name == "Книги"
    assert category.description == "Художественная литература"
    assert len(category._Category__products) == 0
    assert Category.product_count == 0
    assert Category.category_count == 1


def test_category_init_with_products():
    p1 = Product("Война и мир", "Классика", 800, 3)
    p2 = Product("Преступление и наказание", "Классика", 750, 2)
    category = Category("Книги", "Художественная литература", [p1, p2])
    assert len(category._Category__products) == 2
    assert Category.product_count == 2
    assert Category.category_count == 2


def test_add_product_valid():
    category = Category("Электроника", "Гаджеты", [])
    smartphone = Smartphone("Phone X", "Смартфон", 99900, 1, "Android", 6.5)
    category.add_product(smartphone)
    assert len(category._Category__products) == 1
    assert Category.product_count == 3


def test_add_product_invalid_type():
    category = Category("Травы", "Газон", [])
    with pytest.raises(TypeError):
        category.add_product("не продукт")
    assert len(category._Category__products) == 0
    assert Category.product_count == 3


def test_str_representation():
    p1 = Product("Семена газонной травы", "Трава", 500, 4)  # quantity = 4
    p2 = Product("Удобрение", "Садовое", 300, 2)          # quantity = 2
    category = Category("Сад", "Товары для сада", [p1, p2])
    result = str(category)
    assert "Сад" in result
    assert "количество продуктов: 6 шт." in result


def test_products_property():
    p = Product("Чай", "Напитки", 250, 5)
    category = Category("Напитки", "Чай и кофе", [p])
    output = category.products
    assert "Чай" in output
    assert "250 руб." in output
