import arcade
from game import constants
from game.hero import Player
from game.ground import Ground
from game.arcade_output_service import ArcadeOutputService
#from game.move_actors import MoveActors

class Director(arcade.Window):
    """The responsibilty of Director is to create the window, set up the game, and direct the flow of the game. 

    Stereotype:
        Controller, Interfacer

    Attributes:
        output_service: instance of ArcadeOutputService
        player_list (list): Begins with an empty list for player sprites
        wall_list (list): Begins with an empty list for wall sprites 
    """

    def __init__(self):
        """The Class Contructor."""

        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        self.output_service = ArcadeOutputService()

        # Lists of sprites
        self.player_list = None
        self.wall_list = None
        
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Sets up the game.

        Args:
            self (Director): an instance of Director
        """
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

        
        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, constants.GRAVITY)



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Controls player sprite.
        
        Args:
            self (Director): an instance of Director
            key: a key that is pressed
        """
        
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
        #elif key == arcade.key.DOWN or key == arcade.key.S:
            #self.player_sprite.change_y = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. 
        
        Args:
            self (Director): an instance of Director
            key: a key that is released
        """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_draw(self):
        """Handles drawing of actors in game.

        Args:
            self (Director): an instance of Director
        """
        
        self.output_service.clear_screen()
        self.output_service.draw_actors(self.wall_list)
        self.output_service.draw_actors(self.player_list)


    def on_update(self, delta_time):
        """ Movement and game logic. Updates the screen.
        
        Args:
            self (Director): an instance of Director
        """

        # Move the player with the physics engine
        self.physics_engine.update()
