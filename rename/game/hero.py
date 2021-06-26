"""The Player character"""
from game import constants
import arcade

class Player(arcade.Sprite):
    """A code template for the player character. 

     Stereotype:
        Information Holder
    
    Attributes:
        center_x (integer): the x-coordinate of the center of the sprite
        center_y (integer): the y-coordinate of the center of the sprite
    """

    def __init__(self):
        """Class Constructor."""
        super().__init__(constants.PLAYER_IMAGE, constants.CHARACTER_SCALING)

        self.center_x = 50
        self.center_y = 200
        