class Tile:
    def __init__(self, position, layers):
        self._position = position
        self._layers = layers

    def __repr__(self):
        return f"{self.position}:{self.layers}"

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, new_layers):
        self._layers = new_layers

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

class TileGrid:
    def __init__(self, size):
        self._grid = []
        for row_position in range(0, size[0]):
            row = []
            for column_position in range(0, size[1]):
                row.append(Tile((row_position, column_position), []))
            self._grid.append(row)
            row = []

    def __repr__(self):
        return f"{self._grid}"

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid):
        self._grid = new_grid

def fill_grid(grid, tile_type):
    for row in grid.grid:
        for tile in row:
            tile.layers = [tile_type]

def draw_grid(grid, screen, assets, tile_size, cursor_position=None):
    for row_index, row in enumerate(grid.grid):
        for tile_index, tile in enumerate(row):
            screen_position = (tile.position[0] * tile_size[0], tile.position[1] * tile_size[1])
            for layer in tile.layers:
                screen.blit(assets[layer], screen_position)

            if cursor_position == (row_index, tile_index):
                screen.blit(assets["cursor"], screen_position)


def process_structures(grid, stats, STRUCTURE_MAP):
    for row in grid.grid:
        for tile in row:
            for layer in tile.layers:
                if not layer in STRUCTURE_MAP.keys():
                    continue

                if STRUCTURE_MAP[layer]["product"] in stats.keys():
                    stats[STRUCTURE_MAP[layer]["product"]] += STRUCTURE_MAP[layer]["amount"]
                    continue

                stats[STRUCTURE_MAP[layer]["product"]] = STRUCTURE_MAP[layer]["amount"]
