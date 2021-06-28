import arcade
from game import constants
from game.hero import Player
from game.ground import Ground
from game.arcade_output_service import ArcadeOutputService
from game.bullet import Bullet
#from game.move_actors import MoveActors
print
class Director(arcade.Window):


    def __init__(self):

        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        self.output_service = ArcadeOutputService()

        # Lists of sprites
        self.player_list = None
        self.wall_list = None
        self.bullet_list = None
        
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0


        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        #self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list = arcade.SpriteList()

        # Read the map
        map_name = constants.TEST_MAP
        my_map = arcade.tilemap.read_tmx(map_name)

        # Read map layers
        self.wall_list = arcade.tilemap.process_layer(my_map, 'Platforms', constants.TILE_SCALING)


        # Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        
        # Create the ground
        #for x in range(0, 1250, 64):
        #    wall = Ground(x, 32)
        #    self.wall_list.append(wall)

        
        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, constants.GRAVITY)



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
        #elif key == arcade.key.DOWN or key == arcade.key.S:
            #self.player_sprite.change_y = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.J:
            bullet = Bullet(self.player_sprite.right + 20, self.player_sprite.center_y)
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_draw(self):
        
        self.output_service.clear_screen()
        self.output_service.draw_actors(self.wall_list)
        self.output_service.draw_actors(self.player_list)
        self.output_service.draw_actors(self.bullet_list)


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Move the bullets
        self.bullet_list.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + constants.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + constants.SCREEN_WIDTH - constants.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + constants.SCREEN_HEIGHT - constants.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                constants.SCREEN_HEIGHT + self.view_bottom)


        # Get rid of bullets
        

