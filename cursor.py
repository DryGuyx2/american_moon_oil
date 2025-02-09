import pygame

import utils

class Cursor:
    def __init__(self, grid_size):
        self._position = (0, 0)
        self._grid_size = grid_size
        self._height = 0

    def __repr__(self):
        return f"{self._height}:{self._position}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height

def is_touching_edge(position, grid_size, edge):
    if edge == "left":
        return position[0] == 0
    elif edge == "right":
        return position[0] == grid_size[0]
    elif edge == "top":
        return position[1] == 0
    elif edge == "bottom":
        return position[1] == grid_size[1]

    raise NameError("Invalid edge name")

def move_cursor(event, cursor, grid):
    max_cursor_tile_height = len(grid.grid[cursor.position[0]][cursor.position[1]].layers) - 1

    if event.key == pygame.K_RETURN:
        if cursor.height <= 0:
            cursor.height = max_cursor_tile_height
            return
        cursor.height -= 1
        return

    grid_size = (len(grid.grid[0]) - 1, len(grid.grid) - 1)

    if event.key == pygame.K_LEFT and not is_touching_edge(cursor.position, grid_size, "left"):
        cursor.position = (cursor.position[0] - 1, cursor.position[1])
    elif event.key == pygame.K_RIGHT and not is_touching_edge(cursor.position, grid_size, "right"):
        cursor.position = (cursor.position[0] + 1, cursor.position[1])
    elif event.key == pygame.K_UP and not is_touching_edge(cursor.position, grid_size, "top"):
        cursor.position = (cursor.position[0], cursor.position[1] - 1)
    elif event.key == pygame.K_DOWN and not is_touching_edge(cursor.position, grid_size, "bottom"):
        cursor.position = (cursor.position[0], cursor.position[1] + 1)

    cursor.height = len(grid.grid[cursor.position[0]][cursor.position[1]].layers) - 1

def to_grid_position(screen_position, screen_size, grid_size):
    x = utils.scale_number(screen_position[0], (0, screen_size[0]), (0, grid_size[0]))
    y = utils.scale_number(screen_position[1], (0, screen_size[1]), (0, grid_size[1]))
    return (int(round(x, 0)), int(round(y, 0)))
