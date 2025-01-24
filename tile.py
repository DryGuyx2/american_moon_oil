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

def draw_grid(grid, screen, type_to_image_map, tile_size):
    for row in grid.grid:
        for tile in row:
            screen_position = (tile.position[0] * tile_size[0], tile.position[1] * tile_size[1])
            for layer in tile.layers:
                screen.blit(type_to_image_map[layer], screen_position)
