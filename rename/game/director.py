from typing import Optional
from game import constants
from game.player import Player
from game.arcade_output_service import ArcadeOutputService
from game.bullet import Bullet
import os, arcade, math

class MenuView(arcade.View):
    def on_show(self):
        self.background = arcade.load_texture(constants.TITLE_BACKGROUND)
        arcade.set_background_color(arcade.color.WHITE)
        self.music = arcade.Sound(constants.TITLE_MUSIC, streaming=True)
        self.music_player = self.music.play(0.5)
        

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Jumping Bullets", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.music.stop(self.music_player)
        self.window.show_view(game_view)

class EndView(arcade.View):
    def on_show(self):
        self.background = arcade.load_texture(constants.TITLE_BACKGROUND)
        arcade.set_background_color(arcade.color.WHITE)
        self.music = arcade.Sound(constants.END_MUSIC, streaming=True)
        self.music_player = self.music.play(0.5)
        

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Victory!", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to Restart", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.music.stop(self.music_player)
        self.window.show_view(game_view)


    

class GameView(arcade.View):
    """The responsibilty of Director is to create the window, set up the game, and direct the flow of the game. 

    Stereotype:
        Controller, Interfacer

    Attributes:
        output_service: instance of ArcadeOutputService
        player_list (list): Begins with an empty list for player sprites
        wall_list (list): Begins with an empty list for wall sprites 
    """

    def __init__(self):
        # The Class Contructor.

        super().__init__()

        self.output_service = ArcadeOutputService()

        # Lists of sprites
        self.player_list = None
        self.wall_list = None
        self.bullet_list = None
        self.item_list = None
        self.moving_sprites_list = None
        self.music = None
        
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Set the physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Set the level
        self.level = 1
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.map_name = os.path.join(self.PATH, '..', 'maps', f'map{self.level}.tmx')

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.music = arcade.Sound(constants.MAIN_MUSIC, streaming=True)
        self.music_player = self.music.play(0.5)

    def setup(self):
        """Sets up the game.

        Args:
            self (Director): an instance of Director
        """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Read the map
        map_name = self.map_name
        my_map = arcade.tilemap.read_tmx(map_name)
      
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.tilemap.process_layer(my_map, 'Platforms', constants.TILE_SCALING)
        self.item_list = arcade.tilemap.process_layer(my_map, 'Dynamic Items', constants.TILE_SCALING)
        self.ammo_list = arcade.tilemap.process_layer(my_map, 'Ammo', constants.TILE_SCALING)
        self.breakable_wall_list = arcade.tilemap.process_layer(my_map, 'Breakable Walls', constants.TILE_SCALING)
        self.moving_sprites_list = arcade.tilemap.process_layer(my_map, 'Moving Sprites', constants.TILE_SCALING)
        self.spawn_point_list = arcade.tilemap.process_layer(my_map, 'Begin', constants.TILE_SCALING)
        self.health_list = arcade.tilemap.process_layer(my_map, 'Health', constants.TILE_SCALING)
        self.damaging_sprites_list = arcade.tilemap.process_layer(my_map, 'Damaging Sprites', constants.TILE_SCALING)
        try:
            self.exit_point_list = arcade.tilemap.process_layer(my_map, 'Exit', constants.TILE_SCALING)
        except:
            pass
        # self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        # self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        self.player_sprite = Player(self.spawn_point_list[0].center_x, self.spawn_point_list[0].center_y)
        self.player_list.append(self.player_sprite)

        
        # ----Setting up the Physics Engine------
        
        # Set the damping, the amount of velocity the object
        # keeps each second.
        damping = constants.DEFAULT_DAMPING

        # Set the gravity
        gravity = (0, -constants.GRAVITY)
        
        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)

        # ---------- Add Collision Handlers --------
        
        # Bullet/wall collision
        def wall_hit_handler(bullet_sprite, wall_sprite, _arbiter, _space, _data):
            # Bullet wall collision
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        # Bullet/item collision
        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            # Bullet Item collision
            bullet_sprite.remove_from_sprite_lists()
        
        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)

        # Bullet/ammo collision
        def ammo_hit_handler(bullet_sprite, ammo_sprite, _arbiter, _space, _data):
            # Bullet ammo collision
            bullet_sprite.remove_from_sprite_lists()
        
        self.physics_engine.add_collision_handler("bullet", "ammo", post_handler=ammo_hit_handler)

        # Bullet/health collision
        def health_hit_handler(bullet_sprite, health_sprite, _arbiter, _space, _data):
            # Bullet health collision
            bullet_sprite.remove_from_sprite_lists()
        
        self.physics_engine.add_collision_handler("bullet", "health", post_handler=health_hit_handler)

        # Bullet/breakable wall collision
        def breakable_wall_hit_handler(bullet_sprite, wall_sprite, _arbiter, _space, _data):
            # Bullet on breakable wall collision
            bullet_sprite.remove_from_sprite_lists()
            wall_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "breakable wall", post_handler=breakable_wall_hit_handler)

        # Bullet/enemy collision
        def enemy_hit_handler(bullet_sprite, enemy_sprite, _arbiter, _space, _data):
            # Bullet on enemy collision
            bullet_sprite.remove_from_sprite_lists()
            enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "damage", post_handler=enemy_hit_handler)

        # Bullet/exit point collisions
        def bullet_exit_handler(bullet_sprite, exit_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "exit", post_handler=bullet_exit_handler)

        # Add ammo pickup collisions
        def player_item_ammo_handler(player_sprite, item_sprite, _arbiter, _space, _data):
            player_sprite.ammo += 5
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "ammo", post_handler=player_item_ammo_handler)

        # Add exit point collisions
        def player_exit_handler(player_sprite, exit_sprite, _arbiter, _space, _data):
            if self.level <= 2:
                self.go_to_next_level()
            else:
                end_view = EndView()
                self.music.stop(self.music_player)
                self.window.show_view(end_view)

        self.physics_engine.add_collision_handler("player", "exit", post_handler=player_exit_handler)

        # Add health pickup collisions
        def player_item_health_handler(player_sprite, item_sprite, _arbiter, _space, _data):
            item_sprite.remove_from_sprite_lists()
            if player_sprite.health < 100:
                player_sprite.health += 5
                if player_sprite.health > 100:
                    player_sprite.health = 100

        self.physics_engine.add_collision_handler("player", "health", post_handler=player_item_health_handler)

        # Add damaging sprite collisions
        def player_damage_sprite_collision(player_sprite, damage_sprite, _arbiter, _space, _data):
            player_sprite.health -= 1
            
        self.physics_engine.add_collision_handler("player", "damage", post_handler=player_damage_sprite_collision)

        # Add the player
        self.physics_engine.add_sprite(self.player_sprite, friction=constants.PLAYER_FRICTION,
                                       mass=constants.PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=constants.PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=constants.PLAYER_MAX_VERTICAL_SPEED)
        
        # Add the walls
        self.physics_engine.add_sprite_list(self.wall_list, friction=constants.WALL_FRICTION, collision_type="wall", body_type=arcade.PymunkPhysicsEngine.STATIC)
        
        # Add the items
        self.physics_engine.add_sprite_list(self.item_list, friction=constants.DYNAMIC_ITEM_FRICTION, collision_type="item")

        # Add breakable walls
        self.physics_engine.add_sprite_list(self.breakable_wall_list, friction=constants.WALL_FRICTION, collision_type="breakable wall", body_type=arcade.PymunkPhysicsEngine.STATIC)
        
        # Add moving platforms
        self.physics_engine.add_sprite_list(self.moving_sprites_list, body_type=arcade.PymunkPhysicsEngine.KINEMATIC, collision_type="wall")

        # Add the ammunition items
        self.physics_engine.add_sprite_list(self.ammo_list, collision_type="ammo", body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Add health items
        self.physics_engine.add_sprite_list(self.health_list, collision_type="health", body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Add the exit point
        try:
            self.physics_engine.add_sprite(self.exit_point_list[0], friction=constants.FLAG_FRICTION, collision_type='exit', gravity=(0, 0))
        except:
            pass

        # Add damage sprites
        self.physics_engine.add_sprite_list(self.damaging_sprites_list, collision_type="damage", body_type=arcade.PymunkPhysicsEngine.KINEMATIC)


    def go_to_next_level(self):
        self.level += 1
        self.map_name = os.path.join(self.PATH, '..', 'maps', f'map{self.level}.tmx')
        self.setup()

    

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Controls player sprite.
        
        Args:
            self (Director): an instance of Director
            key: a key that is pressed
        """
        
       
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.player_sprite.look_left()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.player_sprite.look_right()
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            # Check if player is on the ground then jump
            if self.physics_engine.is_on_ground(self.player_sprite):
                impulse = (0, constants.PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
                arcade.play_sound(constants.JUMP_SOUND)
        elif key == arcade.key.J:
            if self.player_sprite.ammo > 0:
                bullet = Bullet(20, 5, arcade.color.BLACK)
                self.bullet_list.append(bullet)
                arcade.play_sound(constants.SHOOT_SOUND)

                # Set bullet position away from the way the player is facing
                start_y = self.player_sprite.center_y
                if self.player_sprite.face_left:
                    start_x = self.player_sprite.left - 20
                    dest_x = self.player_sprite.center_x - 400
                    angle = 180
                else:
                    start_x = self.player_sprite.right + 20
                    dest_x = self.player_sprite.center_x + 400
                    angle = 0


                # size = max(self.player_sprite.width, self.player_sprite.height) / 2

                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = angle

                # Set bullet gravity
                bullet_gravity = (0, -constants.BULLET_GRAVITY)

                # Add bullet sprite
                self.physics_engine.add_sprite(bullet, mass=constants.BULLET_MASS,
                                                damping=1.0, friction=0.0,
                                                collision_type="bullet",
                                                gravity=bullet_gravity,
                                                elasticity=0.0)
                
                # Add force to bullet
                force = (constants.BULLET_MOVE_FORCE, 0)
                self.physics_engine.apply_force(bullet, force)

                # Subtract a ammo from the player
                self.player_sprite.ammo -= 1

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. 
        
        Args:
            self (Director): an instance of Director
            key: a key that is released
        """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_draw(self):
        """Handles drawing of actors in game.

        Args:
            self (Director): an instance of Director
        """
        
        self.output_service.clear_screen()
        self.output_service.draw_actors(self.wall_list)
        self.output_service.draw_actors(self.player_list)
        self.output_service.draw_actors(self.bullet_list)
        self.output_service.draw_actors(self.item_list)
        self.output_service.draw_actors(self.breakable_wall_list)
        self.output_service.draw_actors(self.moving_sprites_list)
        self.output_service.draw_actors(self.ammo_list)
        self.output_service.draw_actors(self.exit_point_list)
        self.output_service.draw_actors(self.health_list)
        self.output_service.draw_actors(self.damaging_sprites_list)
        health_position = self.player_sprite.get_health_coordinates()
        health_display = f"Health: {self.player_sprite.health}"
        arcade.draw_text(health_display, health_position[0], health_position[1], arcade.color.BLACK, 10)
        ammo_position = self.player_sprite.get_ammo_display_coordinates()
        ammo_display = f"Ammo: {self.player_sprite.ammo}"
        arcade.draw_text(ammo_display, ammo_position[0], ammo_position[1], arcade.color.BLACK, 10)

    def apply_force(self, is_on_ground, sprite):
        # Update forces based on input
        force1 = constants.PLAYER_MOVE_FORCE_ON_GROUND
        if self.left_pressed and not self.right_pressed:
            # Create and apply force to the left
            force1 *= -1
            if not is_on_ground:
                force1 /= 2
        elif self.right_pressed and not self.left_pressed:
            # Create and apply force to the right
            if not is_on_ground:
                force1 /= 2
        else:
            # Increase friction to stop moving
            self.physics_engine.set_friction(sprite, 1.0)
            return
        self.physics_engine.set_friction(sprite, 0)
        self.physics_engine.apply_force(sprite, (force1, 0))


    def on_update(self, delta_time):
        """ Movement and game logic. Updates the screen.
        
        Args:
            self (Director): an instance of Director
        """

        self.apply_force(self.physics_engine.is_on_ground(self.player_sprite), self.player_sprite)
        
        # ------ Manage Scrolling ------

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
            # Only scroll to integers. Otherwise we end up with pixels that don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left, constants.SCREEN_WIDTH + self.view_left, self.view_bottom, constants.SCREEN_HEIGHT + self.view_bottom)

        # Check boundaries for each moving sprite and reverse
        for moving_sprite in self.moving_sprites_list:
            if moving_sprite.boundary_right and moving_sprite.change_x > 0 and moving_sprite.right > moving_sprite.boundary_right:
                moving_sprite.change_x *= -1
            elif moving_sprite.boundary_left and moving_sprite.change_x < 0 and moving_sprite.left < moving_sprite.boundary_left:
                moving_sprite.change_x *= -1
            if moving_sprite.boundary_top and moving_sprite.change_y > 0 and moving_sprite.top > moving_sprite.boundary_top:
                moving_sprite.change_y *= -1
            elif moving_sprite.boundary_bottom and moving_sprite.change_y < 0 and moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1

            # Figure out and set our moving sprites velocity.
            velocity = (moving_sprite.change_x * 100, moving_sprite.change_y * 100)
            self.physics_engine.set_velocity(moving_sprite, velocity)
        
        # Check boundaries for each moving sprite and reverse
        
        for moving_damage_sprite in self.damaging_sprites_list:
            if moving_damage_sprite.boundary_right and moving_damage_sprite.change_x > 0 and moving_damage_sprite.right > moving_damage_sprite.boundary_right:
                moving_damage_sprite.change_x *= -1
            elif moving_damage_sprite.boundary_left and moving_damage_sprite.change_x < 0 and moving_damage_sprite.left < moving_damage_sprite.boundary_left:
                moving_damage_sprite.change_x *= -1
            if moving_damage_sprite.boundary_top and moving_damage_sprite.change_y > 0 and moving_damage_sprite.top > moving_damage_sprite.boundary_top:
                moving_damage_sprite.change_y *= -1
            elif moving_damage_sprite.boundary_bottom and moving_damage_sprite.change_y < 0 and moving_damage_sprite.bottom < moving_damage_sprite.boundary_bottom:
                moving_damage_sprite.change_y *= -1

            # Figure out and set our moving enemies velocity.
            velocity = (moving_damage_sprite.change_x * 100, moving_damage_sprite.change_y * 100)
            self.physics_engine.set_velocity(moving_damage_sprite, velocity)
        
        # Move everything with the physics engine
        self.physics_engine.step()
        

        # Reset the game if the player health reaches 0
        if self.player_sprite.health <= 0:
            self.setup()

        # Reset if the player is out of bounds
        if self.player_sprite.center_y < -200:
            self.setup()

        


def run():
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, "Jumping Bullets")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()