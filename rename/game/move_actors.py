import arcade
from game import constants

#class MoveActors:
#
#    def __init__(self, player_sprite, wall_list):
#        
#        self.physics_engine = arcade.PhysicsEngineSimple(player_sprite, wall_list)
#
#
#    def on_key_press(self, key, modifiers):
#        """Called whenever a key is pressed. """
#
#        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
#            self.player_sprite.change_y = constants.PLAYER_MOVEMENT_SPEED
#        elif key == arcade.key.DOWN or key == arcade.key.S:
#            self.player_sprite.change_y = -constants.PLAYER_MOVEMENT_SPEED
#        elif key == arcade.key.LEFT or key == arcade.key.A:
#            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
#        elif key == arcade.key.RIGHT or key == arcade.key.D:
#            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
#
#    def on_key_release(self, key, modifiers):
#        """Called when the user releases a key. """
#
#        if key == arcade.key.UP or key == arcade.key.W:
#            self.player_sprite.change_y = 0
#        elif key == arcade.key.DOWN or key == arcade.key.S:
#            self.player_sprite.change_y = 0
#        elif key == arcade.key.LEFT or key == arcade.key.A:
#            self.player_sprite.change_x = 0
#        elif key == arcade.key.RIGHT or key == arcade.key.D:
#            self.player_sprite.change_x = 0
#
#    def get_physics_engine(self):
#        """ Movement and game logic """
#
#        
#        return self.physics_engine