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


    @property
    def products(self):
        product_str = ''
        for prod in self.__products:
            product_str += f'{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт. \n'
        return product_str

