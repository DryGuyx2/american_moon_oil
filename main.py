import sys

import pygame
import gif_pygame

import utils
import tile
import selection
import structure
import visual

# Configure grid, and screen size
# Tile sizes are automatically scaled accordingly
GAME_SIZE = (320, 320)
GRID_SIZE = (10, 10)
SIZE_MULTIPLIER = 2
SCREEN_SIZE = (GAME_SIZE[0] * SIZE_MULTIPLIER, GAME_SIZE[1] * SIZE_MULTIPLIER)

TILE_SIZE = (32, 32)
TILE_IMAGE_SIZE = TILE_SIZE

STRUCTURE_SELECTION_BAR_POSITION = (140, 260)
SELECTION_BAR_SIZE = (80, 40)
SELECTION_ICON_SIZE = (14, 14)
SELECTION_FRAME_SIZE = (20, 20)

STAT_DISPLAY_SIZE = (144, 96)
TEXT_SIZE = 12

PRODUCTION_TIME = 2
FRAMERATE = 60

pygame.init()

# Load assets
assets = {
    "moon_floor": {"surface": pygame.image.load("assets/moon_floor.png"), "type": "image"},
    "rocket": {"surface": pygame.image.load("assets/rocket.png"), "type": "image"},
    "cursor": {"surface": pygame.image.load("assets/cursor.png"), "type": "image"},
    "oil_pump": {"surface": gif_pygame.load("assets/oil_pump.gif"), "type": "animation"},
    "stat_display": {"surface": pygame.image.load("assets/stat_display.png"), "type": "image"},
    "font": pygame.font.Font("assets/nintendo-nes-font.ttf", TEXT_SIZE),
    "selection_frame": {"surface": pygame.image.load("assets/selection_frame.png"), "type": "image"},
    "selection_bar": {"surface": pygame.image.load("assets/selection_bar.png"), "type": "image"},
    "selection": {
        "oil_pump": {"surface": pygame.image.load("assets/oil_pump_selection.png"), "type": "image"},
        "oil_container": {"surface": pygame.image.load("assets/oil_container_selection.png"), "type": "image"},
    },
}

# Specify tile images to be scaled to the correct size
tile_sprites = {
    "moon_floor": (1, 1),
    "oil_pump": (1, 1),
    "rocket": (1, 2),
}

# Scale all the tile images
for tile_sprite, size in tile_sprites.items():
    utils.scale_tile_sprite(assets[tile_sprite], size, TILE_IMAGE_SIZE)

# Scale stat display
assets["stat_display"]["surface"] = pygame.transform.scale(assets["stat_display"]["surface"], STAT_DISPLAY_SIZE)

# Scale selection items
assets["selection_bar"]["surface"] = pygame.transform.scale(assets["selection_bar"]["surface"], SELECTION_BAR_SIZE)
assets["selection_frame"]["surface"] = pygame.transform.scale(assets["selection_frame"]["surface"], SELECTION_FRAME_SIZE)

for selection_icon in assets["selection"].keys():
    surface = assets["selection"][selection_icon]["surface"]
    assets["selection"][selection_icon]["surface"] = pygame.transform.scale(surface, SELECTION_ICON_SIZE)

STRUCTURE_MAP = {
    "oil_pump": structure.Structure(
        name="oil_pump",
        products=[("oil", 50)],
        build_resources=[("funds", 50)],
        consumption=[],
        ),
    "rocket": structure.Structure(
        name="rocket",
        products=[("funds", 50)],
        build_resources=[],
        consumption=[("oil", 50)],
        buildable=False,
        ),
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
tile_cursor = selection.Cursor(GRID_SIZE)

# Initialize structure selection
buildable_structures = [name for name, structure in STRUCTURE_MAP.items() if structure.buildable]
buildable_structures.append("oil_container")
structure_selection = selection.StructureSelection(buildable_structures)

# Set up pygame

clock = pygame.time.Clock()

internal_surface = pygame.Surface(GAME_SIZE)
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
            tile_cursor.position = selection.to_grid_position(screen_position, SCREEN_SIZE, grid_size)

        selected_tile = grid.grid[tile_cursor.position[0]][tile_cursor.position[1]]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                structure.build_structure(stats, "oil_pump", selected_tile, structure_map)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                structure.build_structure(stats, "oil_pump", selected_tile, structure_map)
                return

            if event.key == pygame.K_RIGHT:
                selection.move_selection_position(structure_selection, 1)
                print(f"Selection: {structure_selection}")
                return

            if event.key == pygame.K_LEFT:
                selection.move_selection_position(structure_selection, -1)
                print(f"Selection: {structure_selection}")
                return

        if event.type == PRODUCTION_UPDATE_EVENT:
            structure.process_structures(grid, stats, structure_map)
            #print(f"Stats: {stats}")
        #print(f"Cursor: {tile_cursor}")

PRODUCTION_UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PRODUCTION_UPDATE_EVENT, PRODUCTION_TIME * 1000)

print(SCREEN_SIZE)
while True:
    handle_events(STRUCTURE_MAP)

    screen.fill((0, 0, 0))
    visual.draw_tilegrid(grid.grid, internal_surface, assets, TILE_SIZE, cursor_position=tile_cursor.position)
    visual.draw_stats(internal_surface, stats, assets, (3, 3), GAME_SIZE, STAT_DRAW_COLORS)
    structure_selection_surface = visual.render_structure_selection(structure_selection, assets)
    internal_surface.blit(structure_selection_surface, STRUCTURE_SELECTION_BAR_POSITION)

    screen.blit(pygame.transform.scale(internal_surface, SCREEN_SIZE), (0, 0))
    pygame.display.flip()
