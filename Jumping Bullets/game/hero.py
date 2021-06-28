"""The Player character"""
from game import constants
import arcade

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(constants.PLAYER_IMAGE, constants.CHARACTER_SCALING)

        self.center_x = 50
        self.center_y = 200
        