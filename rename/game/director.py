import arcade
from game import constants
from game.hero import Player
from game.ground import Ground

class Director(arcade.Window):


    def __init__(self):

        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        # Lists of sprites
        self.player_list = None
        self.wall_list = None
        

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1250, 64):
            wall = Ground(x, 32)
            self.wall_list.append(wall)

    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()
        self.player_list.draw()

