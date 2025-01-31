import sys

import pygame

# import utils
import tile
import cursor

# Configure grid, and screen size
# Tile sizes are automatically scaled accordingly
SCREEN_SIZE = (640, 640)
GRID_SIZE = (5, 5)
TILE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
TILE_IMAGE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])

PRODUCTION_TIME = 2
FRAMERATE = 60

pygame.init()

# Load assets
assets = {
    "moon_floor": pygame.image.load("assets/moon_floor.png"),
    "oil_pump": pygame.image.load("assets/oil_pump.png"),
    "cursor": pygame.image.load("assets/cursor.png"),
    "font": pygame.font.Font("assets/nintendo-nes-font.ttf", 32),
}

# Specify tile images to be scaled to the same size
tile_sprites = [
    "moon_floor",
    "oil_pump",
]

# Scale all the tile images
for tile_sprite in tile_sprites:
    assets[tile_sprite] = pygame.transform.scale(assets[tile_sprite], TILE_IMAGE_SIZE)

STRUCTURE_MAP = {
    "oil_pump": {"product": "oil", "amount": 3},
}

stats = {}

# Initialize grid with moon floor tile sprite as bottom layer
grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, "moon_floor")
grid.grid[0][0].layers.append("oil_pump")
#print(f"Grid:\n{grid}")

# Initialize cursor
tile_cursor = cursor.Cursor(GRID_SIZE)

# Set up pygame

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("American Moon Oil")

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == PRODUCTION_UPDATE_EVENT:
            tile.process_structures(grid, stats, STRUCTURE_MAP)
            print(f"Stats: {stats}")

        selected_tile = grid.grid[tile_cursor.position[0]][tile_cursor.position[1]]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if not "oil_pump" in selected_tile.layers:
                    selected_tile.layers.append("oil_pump")
                return

            cursor.move_cursor(event, tile_cursor, grid)
            print(f"Cursor: {tile_cursor}")

def draw_stats(stats, assets):
    stat_position_y = 0
    for stat, value in stats.items():
        text = assets["font"].render(f"{stat}: {value}", False, (255, 255, 255))
        position = (0, stat_position_y * SCREEN_SIZE[1] // 10)
        screen.blit(text, position)
        stat_position_y += 1

PRODUCTION_UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PRODUCTION_UPDATE_EVENT, PRODUCTION_TIME * 1000)

while True:
    handle_events()

    screen.fill((0, 0, 0))
    tile.draw_grid(grid, screen, assets, TILE_SIZE, cursor_position=tile_cursor.position)
    draw_stats(stats, assets)

    pygame.display.flip()
