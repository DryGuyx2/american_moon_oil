import pygame
import sys

import utils
import tile

GRID_SIZE = (5, 5)

grid = tile.TileGrid(GRID_SIZE)
tile.fill_grid(grid, tile.TILETYPES[0])

print(f"Grid:\n{grid}")


FRAMERATE = 60

pygame.init()

clock = pygame.time.Clock()

SCREEN_SIZE = (500, 500)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("American Moon Oil")


TILE_SIZE = (SCREEN_SIZE[0] // GRID_SIZE[0], SCREEN_SIZE[1] // GRID_SIZE[1])

tile_to_image_map = {
    "moon_floor": pygame.image.load("assets/white_square.jpg"),
}

for image in tile_to_image_map.values():
    pygame.transform.scale(image, (TILE_SIZE[0], TILE_SIZE[1]))

while True:
    screen.fill((0, 0, 0))
    tile.draw_grid(grid, screen, tile_to_image_map, TILE_SIZE)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FRAMERATE)