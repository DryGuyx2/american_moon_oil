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
    # Draw order is a nested list structure where
    # every sub-list contains a tile image,
    # with a screen position
    # Every tile in each layer is then
    # drawn in order based on the layer position in the list
    draw_order = []

    # Here we set up the layers, and tiles
    for row_index, row in enumerate(grid.grid):
        for tile_index, tile in enumerate(row):
            screen_position = (tile.position[0] * tile_size[0], tile.position[1] * tile_size[1])
            for layer_index, layer in enumerate(tile.layers):

                if layer_index == 0:
                    draw_order.append([])

                # Here we add the tile to the correct layer index in the draw order list
                draw_order[layer_index].append((assets[layer], screen_position))
            # After setting up all the tiles, we finally place the cursor at the top of its position
            if cursor_position == (row_index, tile_index):
                top_layer = len(grid.grid[row_index][tile_index].layers) - 1
                draw_order[top_layer].append((assets["cursor"], screen_position))

    # Here we draw the tiles
    for layer in draw_order:
        for tile in layer:
            screen.blit(tile[0], tile[1])
