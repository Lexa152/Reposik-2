def test_cat_init(cat1):
    assert cat1.name == 'Фрукты'
    assert cat1.description == 'продукты, богатые клетчаткой и витаминами'
    assert len(cat1.products) == 3
    assert cat1.product_count == 3
    assert cat1.category_count == 1
