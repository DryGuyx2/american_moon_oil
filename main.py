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

FRAMERATE = 60

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

        if event.type == pygame.KEYDOWN:
            cursor.move_cursor(event, tile_cursor, grid)
            print(f"Cursor: {tile_cursor}")

while True:
    handle_events()

    screen.fill((0, 0, 0))
    tile.draw_grid(grid, screen, assets, TILE_SIZE, cursor_position=tile_cursor.position)

    pygame.display.flip()

    clock.tick(FRAMERATE)
