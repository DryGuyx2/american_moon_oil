import tile

GRID_SIZE = (5, 5)

grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, tile.TILETYPES[0])

print(f"Grid:\n{grid}")