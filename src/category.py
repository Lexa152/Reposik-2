class Category:
    name: str
    description: str = "без комментариев"
    products = None
    product_count = 0
    category_count = 0


    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        if products is None:
            self.products = []
        else:
            self.products = list(products)
        # Обновляем счётчики класса
        Category.category_count += 1
        self.product_count += len(self.products)
