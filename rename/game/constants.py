import os
import arcade

# Size of grid to show on screen
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Jumping Bullets"

# ------ Player Movement ------------
# Gravity, higher is heavier
GRAVITY = 2000
# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 3000

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 900

# Jump
PLAYER_JUMP_IMPULSE = 1800

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 1.3

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Constants used to scale our sprites from their original size
SPRITE_IMAGE_SIZE = 128
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * CHARACTER_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 150


#-------- Bullet --------
BULLET_MOVE_FORCE = 6500
BULLET_MASS = 0.1
BULLET_GRAVITY = 30

#-----Maps, images, sounds--------------------
PATH = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'player_stand.png')
GROUND_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'stoneMid.png')
SHOOT_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'fall3.wav'))
JUMP_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'jump4.wav'))



# Maps
#MAP_NAME = os.path.join(PATH, '..', f'map{level}.tmx')