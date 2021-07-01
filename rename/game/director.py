import os
import arcade
import math
from typing import Optional
from game import constants
from game.hero import Player
#from game.ground import Ground
from game.arcade_output_service import ArcadeOutputService
from game.bullet import Bullet
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
        self.bullet_list = None
        self.item_list = None
        self.moving_sprites_list = None
        
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
        
        PATH = os.path.dirname(os.path.abspath(__file__))
        self.map_name = os.path.join(PATH, '..', f'map{self.level}.tmx')

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Sets up the game.

        Args:
            self (Director): an instance of Director
        """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
      
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        #self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list = arcade.SpriteList()

        # Read the map
        map_name = self.map_name
        my_map = arcade.tilemap.read_tmx(map_name)

        # Read map layers
        self.wall_list = arcade.tilemap.process_layer(my_map, 'Platforms', constants.TILE_SCALING)
        self.item_list = arcade.tilemap.process_layer(my_map, 'Dynamic Items', constants.TILE_SCALING)
        self.ammo_list = arcade.tilemap.process_layer(my_map, 'Ammo', constants.TILE_SCALING)
        self.breakable_wall_list = arcade.tilemap.process_layer(my_map, 'Breakable Walls', constants.TILE_SCALING)
        self.moving_sprites_list = arcade.tilemap.process_layer(my_map, 'Moving Sprites', constants.TILE_SCALING)
        self.spawn_point_list = arcade.tilemap.process_layer(my_map, 'Begin', constants.TILE_SCALING)
        self.exit_point_list = arcade.tilemap.process_layer(my_map, 'Exit', constants.TILE_SCALING)
        self.health_list = arcade.tilemap.process_layer(my_map, 'Health', constants.TILE_SCALING)
        self.damaging_sprites_list = arcade.tilemap.process_layer(my_map, 'Damaging Sprites', constants.TILE_SCALING)

        # Set up the player
        self.player_sprite = Player(self.spawn_point_list[0].center_x, self.spawn_point_list[0].center_y)
        self.player_list.append(self.player_sprite)

        
        #----Setting up the Physics Engine------
        
        # Set the damping, the amount of velocity the object
        # keeps each second.
        damping = constants.DEFAULT_DAMPING

        # Set the gravity
        gravity = (0, -constants.GRAVITY)
        
        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping = damping, gravity = gravity)

        # ---------- Add Collision Handlers --------
        
        # Bullet/wall collision
        def wall_hit_handler(bullet_sprite, wall_sprite, _arbiter, _space, _data):
            """Bullet wall collision"""
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler = wall_hit_handler)

        # Bullet/item collision
        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            """Bullet Item collision"""
            bullet_sprite.remove_from_sprite_lists()
            item_sprite.remove_from_sprite_lists()
        
        self.physics_engine.add_collision_handler("bullet", "item", post_handler = item_hit_handler)

        # Bullet/breakable wall collision
        def breakable_wall_hit_handler(bullet_sprite, wall_sprite, _arbiter, _space, _data):
            """Bullet on breakable wall collision"""
            bullet_sprite.remove_from_sprite_lists()
            wall_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "breakable wall", post_handler = breakable_wall_hit_handler)

        # Add ammo pickup collisions
        def player_item_ammo_handler(player_sprite, item_sprite, _arbiter, _space, _data):
            player_sprite.ammo += 5
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "ammo", post_handler = player_item_ammo_handler)

        # Add exit point collisions
        def player_exit_handler(player_sprite, exit_sprite, _arbiter, _space, _data):
            self.go_to_next_level()

        self.physics_engine.add_collision_handler("player", "exit", post_handler = player_exit_handler)

        # Add health pickup collisions
        def player_item_health_handler(player_sprite, item_sprite, _arbiter, _space, _data):
            player_sprite.health += 5
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "health", post_handler = player_item_health_handler)

        # Add damaging sprite collisions
        def player_damage_sprite_collision(player_sprite, damage_sprite, _arbiter, _space, _data):
            player_sprite.health -= 5
            
        self.physics_engine.add_collision_handler("player", "damage", post_handler = player_damage_sprite_collision)


        # Add the player
        self.physics_engine.add_sprite(self.player_sprite, friction = constants.PLAYER_FRICTION,
                                        mass = constants.PLAYER_MASS,
                                        moment = arcade.PymunkPhysicsEngine.MOMENT_INF,
                                        collision_type = "player",
                                        max_horizontal_velocity = constants.PLAYER_MAX_HORIZONTAL_SPEED,
                                        max_vertical_velocity = constants.PLAYER_MAX_VERTICAL_SPEED)
        
        # Add the walls
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction = constants.WALL_FRICTION,
                                            collision_type = "wall",
                                            body_type = arcade.PymunkPhysicsEngine.STATIC)
        
        # Add the items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction = constants.DYNAMIC_ITEM_FRICTION,
                                            collision_type = "item")

        # Add breakable walls
        self.physics_engine.add_sprite_list(self.breakable_wall_list,
                                            friction = constants.WALL_FRICTION,
                                            collision_type = "breakable wall",
                                            body_type = arcade.PymunkPhysicsEngine.STATIC)
        
        # Add moving platforms
        self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                            body_type = arcade.PymunkPhysicsEngine.KINEMATIC)

        # Add the ammunition items
        self.physics_engine.add_sprite_list(self.ammo_list, collision_type = "ammo", body_type = arcade.PymunkPhysicsEngine.STATIC)

        # Add health items
        self.physics_engine.add_sprite_list(self.health_list, collision_type = "health", body_type = arcade.PymunkPhysicsEngine.STATIC)

        # Add the exit point
        self.physics_engine.add_sprite_list(self.exit_point_list, friction = constants.WALL_FRICTION, collision_type = 'exit')

        # Add damage sprites
        self.physics_engine.add_sprite_list(self.damaging_sprites_list, collision_type = "damage", body_type = arcade.PymunkPhysicsEngine.KINEMATIC)


    def go_to_next_level(self):
        self.level += 1
        PATH = os.path.dirname(os.path.abspath(__file__))
        self.map_name = os.path.join(PATH, '..', f'map{self.level}.tmx')
        self.setup()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Controls player sprite.
        
        Args:
            self (Director): an instance of Director
            key: a key that is pressed
        """
        
       
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.player_sprite.face_left = True
            self.player_sprite.face_right = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.player_sprite.face_left = False
            self.player_sprite.face_right = True
        elif key == arcade.key.UP or key == arcade.key.W:
            # Check if player is on the ground then jump
            if self.physics_engine.is_on_ground(self.player_sprite):
                impulse = (0, constants.PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
        elif key == arcade.key.J:
            if self.player_sprite.ammo > 0:
                bullet = Bullet(20, 5, arcade.color.BLACK)
                self.bullet_list.append(bullet)


                # Set bullet position based on which way the player is facing
                # Away from the player
                start_y = self.player_sprite.center_y
                if self.player_sprite.face_left:
                    start_x = self.player_sprite.left - 20
                    dest_x = self.player_sprite.center_x - 400
                    angle = 180
                else:
                    start_x = self.player_sprite.right + 20
                    dest_x = self.player_sprite.center_x + 400
                    angle = 0


                #size = max(self.player_sprite.width, self.player_sprite.height) / 2

                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = angle

                # Set bullet gravity
                bullet_gravity = (0, -constants.BULLET_GRAVITY)

                # Add bullet sprite
                self.physics_engine.add_sprite(bullet, mass = constants.BULLET_MASS,
                                                damping = 1.0, friction = 0.6,
                                                collision_type = "bullet",
                                                gravity = bullet_gravity,
                                                elasticity = 0.9)
                
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


        

    def on_update(self, delta_time):
        """ Movement and game logic. Updates the screen.
        
        Args:
            self (Director): an instance of Director
        """

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        
        # Update player forces based on input
        if self.left_pressed and not self.right_pressed:
            # Create left force and apply to player
            if is_on_ground:
                force = (-constants.PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-constants.PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set player friction to 0 while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create right force and apply to player
            if is_on_ground:
                force = (constants.PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (constants.PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set player friction to 0 while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            # Increase player friction to stop moving
            self.physics_engine.set_friction(self.player_sprite, 1.0)
        
        
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
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                constants.SCREEN_HEIGHT + self.view_bottom)

        # Move the player with the physics engine
        self.physics_engine.step()


        # Check boundaries for each moving sprite and reverse
        for moving_sprite in self.moving_sprites_list:
            if moving_sprite.boundary_right and \
                    moving_sprite.change_x > 0 and \
                    moving_sprite.right > moving_sprite.boundary_right:
                moving_sprite.change_x *= -1
            elif moving_sprite.boundary_left and \
                    moving_sprite.change_x < 0 and \
                    moving_sprite.left < moving_sprite.boundary_left:
                moving_sprite.change_x *= -1
            if moving_sprite.boundary_top and \
                    moving_sprite.change_y > 0 and \
                    moving_sprite.top > moving_sprite.boundary_top:
                moving_sprite.change_y *= -1
            elif moving_sprite.boundary_bottom and \
                    moving_sprite.change_y < 0 and \
                    moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1

            # Figure out and set our moving platform velocity.
            velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(moving_sprite, velocity)
        
        # Check boundaries for each moving sprite and reverse
        
        for moving_damage_sprite in self.damaging_sprites_list:
            if moving_damage_sprite.boundary_right and \
                    moving_damage_sprite.change_x > 0 and \
                    moving_damage_sprite.right > moving_damage_sprite.boundary_right:
                moving_damage_sprite.change_x *= -1
            elif moving_damage_sprite.boundary_left and \
                    moving_damage_sprite.change_x < 0 and \
                    moving_damage_sprite.left < moving_damage_sprite.boundary_left:
                moving_damage_sprite.change_x *= -1
            if moving_damage_sprite.boundary_top and \
                    moving_damage_sprite.change_y > 0 and \
                    moving_damage_sprite.top > moving_damage_sprite.boundary_top:
                moving_damage_sprite.change_y *= -1
            elif moving_damage_sprite.boundary_bottom and \
                    moving_damage_sprite.change_y < 0 and \
                    moving_damage_sprite.bottom < moving_damage_sprite.boundary_bottom:
                moving_damage_sprite.change_y *= -1

            # Figure out and set our moving platform velocity.
            velocity = (moving_damage_sprite.change_x * 1 / delta_time, moving_damage_sprite.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(moving_damage_sprite, velocity)
        

        # Reset the game if the player health reaches 0
        if self.player_sprite.health <= 0:
            self.setup()