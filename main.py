import sys

import pygame

# import utils
import tile
import cursor
import structures

# Configure grid, and screen size
# Tile sizes are automatically scaled accordingly
SCREEN_SIZE = (640, 640)
GRID_SIZE = (5, 5)
TILE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
TILE_IMAGE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])

FRAMERATE = 60

STRUCTURE_PRODUCTION_SPEED = 5

# Load assets
assets = {
    "moon_floor": pygame.image.load("assets/moon_floor.png"),
    "oil_pump": pygame.image.load("assets/oil_pump.png"),
    "cursor": pygame.image.load("assets/cursor.png")
}

# Specify tile images to be scaled to the same size
tile_sprites = [
    "moon_floor",
    "oil_pump",
]

# Scale all the tile images
for tile_sprite in tile_sprites:
    assets[tile_sprite] = pygame.transform.scale(assets[tile_sprite], TILE_IMAGE_SIZE)

# Initialize grid with moon floor tile sprite as bottom layer
grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, "moon_floor")
grid.grid[0][0].layers.append("oil_pump")
#print(f"Grid:\n{grid}")

STRUCTURE_MAP = {
    "oil_pump": ("oil", 1)
}
placed_structures = []

# Initialize cursor
tile_cursor = cursor.Cursor(GRID_SIZE)

# Initialize and set up pygame
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("American Moon Oil")

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        selected_tile = grid.grid[tile_cursor.position[0]][tile_cursor.position[1]]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if not "oil_pump" in selected_tile.layers:
                    selected_tile.layers.append("oil_pump")
                    pump_rate = STRUCTURE_MAP["oil_pump"][1]
                    pump_product = STRUCTURE_MAP["oil_pump"][0]
                    oil_pump = structures.Structure("oil_pump", pump_product, pump_rate)
                    placed_structures.append(oil_pump)
                return

            cursor.move_cursor(event, tile_cursor, grid)
            print(f"Cursor: {tile_cursor}")

production_time_left = STRUCTURE_PRODUCTION_SPEED
deltatime = 0
while True:
    deltatime = clock.tick(FRAMERATE)/1000
    #print(f"Deltatime: {deltatime}")
    handle_events()
    production_time_left -= deltatime
    if production_time_left >= 0:
        production_time_left = STRUCTURE_PRODUCTION_SPEED
        products = structures.process_structures(placed_structures)

    screen.fill((0, 0, 0))
    tile.draw_grid(grid, screen, assets, TILE_SIZE, cursor_position=tile_cursor.position)

    pygame.display.flip()
