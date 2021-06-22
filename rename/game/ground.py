from game import constants
import arcade

class Ground(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(constants.GROUND_IMAGE, constants.TILE_SCALING)

        self.center_x = x
        self.center_y = y