class Structure:
    def __init__(self, name, products, build_resources, consumption=None):
        self._name = name
        self._products = products
        self._consumption = consumption
        self._build_resources = build_resources

    @property
    def name(self):
        return self._name

    @property
    def products(self):
        return self._products

    @property
    def consumption(self):
        return self._consumption

    @property
    def build_resources(self):
        return self._build_resources

def build_structure(stats, structure_name, tile, structure_map):
    for layer in tile.layers:
        if layer in structure_map.keys():
            return

    for build_resource, amount in structure_map[structure_name].build_resources:
        if not build_resource in stats.keys():
            return

        if stats[build_resource] < amount:
            return

    for build_resource, amount in structure_map[structure_name].build_resources:
        stats[build_resource] -= amount

    tile.layers.append(structure_name)


def process_structures(grid, stats, structure_map):
    for row in grid.grid:
        for tile in row:
            for layer in tile.layers:
                if not layer in structure_map.keys():
                    continue

                for product, amount in structure_map[layer].products:
                    if product in stats.keys():
                        print(f"{product} in stats, with amount {amount}")
                        stats[product] += amount
                        continue

                    stats[product] = amount
