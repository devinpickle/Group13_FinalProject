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

        self.face_left = False
        self.face_right = True
        
        

    def look_left(self):
        self.face_left = True
        self.face_right = False

    def look_right(self):
        self.face_left = False
        self.face_right = True