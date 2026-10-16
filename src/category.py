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


    def __str__(self):
        total = 0
        for p in self.__products:
            total += p.quantity
        return f"{self.name}, количество продуктов: {total} шт."


    def add_product(self, prod):
        self.__products.append(prod)
        Category.product_count += 1


    @property
    def products(self):
        product_str = ''
        for prod in self.__products:
            product_str += f'{str(prod)}\n'
        return product_str
