class Structure:
    def __init__(self, structure_type, product, rate):
        self._structure_type = structure_type
        self._product = product
        self._rate = rate

    @property
    def structure_type(self):
        return self._structure_type

    @property
    def product(self):
        return self._product

    @property
    def rate(self):
        return self._rate

def process_structures(structures):
    products = {}
    for structure in structures:
        products[structure.product] = structure.rate
    print(f"Produced: {products}")
    return products
