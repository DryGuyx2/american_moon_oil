import pygame

class Cursor:
    def __init__(self, grid_size):
        self._position = (0, 0)
        self._grid_size = grid_size
    
    def __repr__(self):
        return f"{self.position}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

def is_touching_edge(position, grid_size, edge):
    if edge == "left":
        return position[0] == 0
    elif edge == "right":
        return position[0] == grid_size[0] - 1
    elif edge == "top":
        return position[1] == 0
    elif edge == "bottom":
        return position[1] == grid_size[1] - 1
    
    raise NameError("Invalid edge name")

def move_cursor(event, cursor, grid_size):
    if event.key == pygame.K_LEFT and not is_touching_edge(cursor.position, grid_size, "left"):
        cursor.position = (cursor.position[0] - 1, cursor.position[1])
    elif event.key == pygame.K_RIGHT and not is_touching_edge(cursor.position, grid_size, "right"):
        cursor.position = (cursor.position[0] + 1, cursor.position[1])
    elif event.key == pygame.K_UP and not is_touching_edge(cursor.position, grid_size, "top"):
        cursor.position = (cursor.position[0], cursor.position[1] - 1)
    elif event.key == pygame.K_DOWN and not is_touching_edge(cursor.position, grid_size, "bottom"):
        cursor.position = (cursor.position[0], cursor.position[1] + 1)