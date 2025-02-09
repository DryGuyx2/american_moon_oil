import sys

import pygame

# import utils
import tile
import cursor
import structure
import draw

# Configure grid, and screen size
# Tile sizes are automatically scaled accordingly
SCREEN_SIZE = (640, 640)
GRID_SIZE = (5, 5)
TILE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
TILE_IMAGE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
TEXT_SIZE = 28

PRODUCTION_TIME = 2
FRAMERATE = 60

pygame.init()

# Load assets
assets = {
    "moon_floor": pygame.image.load("assets/moon_floor.png"),
    "oil_pump": pygame.image.load("assets/oil_pump.png"),
    "rocket": pygame.image.load("assets/rocket.png"),
    "cursor": pygame.image.load("assets/cursor.png"),
    "font": pygame.font.Font("assets/nintendo-nes-font.ttf", TEXT_SIZE),
}

# Specify tile images to be scaled to the correct size
tile_sprites = {
    "moon_floor": (1, 1),
    "oil_pump": (1, 1),
    "rocket": (1, 2),
}

# Scale all the tile images
for tile_sprite, size in tile_sprites.items():
    scaled_size = (size[0] * TILE_IMAGE_SIZE[0], size[1] * TILE_IMAGE_SIZE[1])
    assets[tile_sprite] = pygame.transform.scale(assets[tile_sprite], scaled_size)

STRUCTURE_MAP = {
    "oil_pump": structure.Structure(name="oil_pump",
                                    products=[("oil", 50)],
                                    build_resources=[("funds", 50)],
                                    consumption=[]),
    "rocket": structure.Structure(name="rocket",
                                  products=[("funds", 50)],
                                  build_resources=[],
                                  consumption=[("oil", 50)]),
}

stats = {
    "funds": 500,
    "oil": 0,
}

STAT_DRAW_COLORS = {
    "funds": (0, 184, 0),
    "oil": (0, 0, 0),
}

# Initialize grid with moon floor tile sprite as bottom layer
grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, "moon_floor")

center_tile = grid.grid[len(grid.grid) // 2][len(grid.grid[0]) // 2]
center_tile.layers.append("rocket")
#print(f"Grid:\n{grid}")

# Initialize cursor
tile_cursor = cursor.Cursor(GRID_SIZE)

# Set up pygame

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("American Moon Oil")

def handle_events(structure_map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            grid_size = (len(grid.grid) - 1, len(grid.grid[0]) - 1)
            screen_position = pygame.mouse.get_pos()
            tile_cursor.position = cursor.to_grid_position(screen_position, SCREEN_SIZE, grid_size)

        if event.type == PRODUCTION_UPDATE_EVENT:
            structure.process_structures(grid, stats, structure_map)
            #print(f"Stats: {stats}")

        selected_tile = grid.grid[tile_cursor.position[0]][tile_cursor.position[1]]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                structure.build_structure(stats, "oil_pump", selected_tile, structure_map)

            cursor.move_cursor(event, tile_cursor, grid)
            #print(f"Cursor: {tile_cursor}")

PRODUCTION_UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PRODUCTION_UPDATE_EVENT, PRODUCTION_TIME * 1000)

while True:
    handle_events(STRUCTURE_MAP)

    screen.fill((0, 0, 0))
    draw.draw_tilegrid(grid.grid, screen, assets, TILE_SIZE, cursor_position=tile_cursor.position)
    draw.draw_stats(screen, stats, assets, SCREEN_SIZE, STAT_DRAW_COLORS)

    pygame.display.flip()
