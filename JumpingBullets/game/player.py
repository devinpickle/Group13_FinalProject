from game import constants
from arcade import load_texture
import arcade

class Player(arcade.Sprite):
    # A code template for the player character. 

    # Stereotype:
    # Information Holder
    
    # Attributes:
    # center_x (integer): the x-coordinate of the center of the sprite
    # center_y (integer): the y-coordinate of the center of the sprite

    def __init__(self, startx, starty):
        # Class Constructor.
        super().__init__(constants.PLAYER_IMAGE, constants.CHARACTER_SCALING)

        self.center_x = startx
        self.center_y = starty

        self.append_texture(load_texture(constants.PLAYER_IMAGE_LEFT))
        self.face_left = False
        self.face_right = True

        self.setup()
    
    def look_left(self):
        self.face_left = True
        self.face_right = False
        self.set_texture(1)
    
    def look_right(self):
        self.face_left = False
        self.face_right = True
        self.set_texture(0)

    def get_health_coordinates(self):
        # Get the coordinates of the health to keep it following the player on screen.
        self.health_x = self.center_x - 30
        self.health_y = self.center_y + 50
        return (self.health_x, self.health_y)

    def get_ammo_display_coordinates(self):
        # Get the coordinates of the health to keep it following the player on screen.
        self.ammo_x = self.center_x - 30
        self.ammo_y = self.center_y + 35
        return (self.ammo_x, self.ammo_y)

    def setup(self):
        # Set player stats
        self.health = 100
        self.ammo = 50