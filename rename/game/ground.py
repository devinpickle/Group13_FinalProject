from game import constants
import arcade

class Ground(arcade.Sprite):
    """A code template for the ground that the player stands on.
    
    Stereotype:
        Information Holder
    
    Attributes:
        center_x (integer): the x-coordinate of the center of the sprite
        center_y (integer): the y-coordinate of the center of the sprite
    """
    def __init__(self, x, y):
        # Class Constructor.
        super().__init__(constants.GROUND_IMAGE, constants.TILE_SCALING)

        self.center_x = x
        self.center_y = y