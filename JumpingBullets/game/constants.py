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
LEFT_VIEWPORT_MARGIN = 800
RIGHT_VIEWPORT_MARGIN = 800
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
SHOOT_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'laser.wav'))
JUMP_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'Digital_SFX', 'phaseJump3.mp3'))
MAIN_MUSIC = os.path.join(PATH, '..', 'assets', 'sounds', 'through space.ogg')
TITLE_MUSIC = os.path.join(PATH, '..', 'assets', 'sounds', 'Space track.mp3')
TITLE_BACKGROUND = os.path.join(PATH, '..', 'assets', 'images', 'scifi_main_menu.jpg')
END_MUSIC = os.path.join(PATH, '..', 'assets', 'sounds', 'snd_music2.ogg')
END_BACKGROUND = os.path.join(PATH, '..', 'assets', 'images', 'rock wall tileset.png')

SLIME_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'impactsplat01.mp3.flac'))
HEALTH_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'life_pickup.flac'))
AMMO_SOUND = arcade.load_sound(os.path.join(PATH, '..', 'assets', 'sounds', 'Digital_SFX', 'phaserDown1.mp3'))

#Enemy Images
BLUE_ALIEN = os.path.join(PATH, '..', 'assets', 'images', 'alien', 'alienBlue_front.png')
PURPLE_SLIME = os.path.join(PATH, '..', 'assets', 'images', 'enemies', 'slimePurple.png')

