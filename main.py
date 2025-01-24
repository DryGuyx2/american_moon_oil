import sys
import pygame

# import utils
import tile
import cursor

GRID_SIZE = (5, 5)
SCREEN_SIZE = (640, 640)
TILE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
TILE_IMAGE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])
FRAMERATE = 60


tile_to_image_map = {
    "moon_floor": pygame.image.load("assets/white_square.jpg"),
    "oil_pump": pygame.image.load("assets/oil_pump.png"),
}

# Scale all tile images to the same size
for key, image in tile_to_image_map.items():
    tile_to_image_map[key] = pygame.transform.scale(image, TILE_IMAGE_SIZE)

# Initialize grid with moon floor tile sprite as bottom layer
grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, "moon_floor")
grid.grid[0][0].layers.append("oil_pump")
print(f"Grid:\n{grid}")

tile_cursor = cursor.Cursor(GRID_SIZE)

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
            max_cursor_height = len(grid.grid[tile_cursor.position[0]][tile_cursor.position[1]].layers) - 1
            cursor.move_cursor(event, tile_cursor, GRID_SIZE, max_cursor_height)
            print(f"Cursor: {tile_cursor}")

while True:
    handle_events()

    screen.fill((0, 0, 0))
    tile.draw_grid(grid, screen, tile_to_image_map, TILE_SIZE)

    pygame.display.flip()

    clock.tick(FRAMERATE)
