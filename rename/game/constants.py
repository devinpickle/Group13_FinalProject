import os
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Jumping Bullets"

# Movement Speed
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.6
PLAYER_JUMP_SPEED = 15
BULLET_SPEED = 25

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 150


PATH = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'player_stand.png')
GROUND_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'stoneMid.png')

# Maps
TEST_MAP = os.path.join(PATH, '..', 'test_map.tmx')