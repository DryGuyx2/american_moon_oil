TILETYPES = [
    "moon_floor"
]

class Tile:
    def __init__(self, position, layers):
        self.position = position
        self.layers = layers
    
    def __repr__(self):
        return f"{self.position}:{self.layers}"
    
    def append_layer(self, layer):
        self.layers.append(layer)
    
    def clear_layers(self):
        self.layers = []

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
            tile.clear_layers()
            tile.append_layer(tile_type)