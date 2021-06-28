import os
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Rename"

# Movement Speed
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.6
PLAYER_JUMP_SPEED = 15

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5


PATH = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'player_stand.png')
GROUND_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'stoneMid.png')