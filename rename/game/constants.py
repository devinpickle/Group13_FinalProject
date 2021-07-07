import os, arcade

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Jumping Bullets"

# Gravity, higher is heavier
GRAVITY = 3000

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 1000
PLAYER_MAX_VERTICAL_SPEED = 2000

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 5000

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 2500

# Jump force
PLAYER_JUMP_IMPULSE = 5000

# Damping - Rate speed is lost after releasing button - Lower is faster
DEFAULT_DAMPING = 0.01

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.6
DYNAMIC_ITEM_FRICTION = 0.6
FLAG_FRICTION = 0.0

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# How many pixels to keep as a minimum margin between the character and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 600
RIGHT_VIEWPORT_MARGIN = 600
BOTTOM_VIEWPORT_MARGIN = 400
TOP_VIEWPORT_MARGIN = 400

# -------- Bullet --------
BULLET_MOVE_FORCE = 1
BULLET_MASS = 0.00001
BULLET_GRAVITY = 0

# ----- Maps, images, and sounds --------------------
PATH = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'player_stand.png')
PLAYER_IMAGE_LEFT = os.path.join(PATH, '..', 'assets', 'images', 'player_stand_left.png')
GROUND_IMAGE = os.path.join(PATH, '..', 'assets', 'images', 'stoneMid.png')
SHOOT_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'fall3.wav'))
JUMP_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'jump4.wav'))