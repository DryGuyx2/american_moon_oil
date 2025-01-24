class Cursor:
    def __init__(self, grid_size):
        self._position = (0, 0)
        self._grid_size = grid_size

    @property
    def position(self):
        return self._position

    @property.setter
    def postion(self, new_position):
        self._position = new_position
