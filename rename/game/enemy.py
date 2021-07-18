from abc import ABC, abstractmethod
import arcade
from arcade.sprite import get_distance_between_sprites
from game import director
#from arcade import load_texture
from game import constants


class Enemy(arcade.Sprite, ABC):
    """A code template for the basic functionality of enemies in-game. Responsible for controlling enemy health, the image to load, the spawning position,
    and so on.
    
    Stereotype:
        Coordinator, Information Holder
    
    Attributes:
        _enemy_health (integer): the amount of health an enemy has
        _enemy_move_speed (integer): the speed of enemy movement (autonomous)
        _enemy_attacking_move_speed (integer): the speed of enemy movement when attacking
        _enemy_sprite (image): the image to load for the enemy

        center_x (integer): the x-coordinate of the center of the sprite
        center_y (integer): the y-coordinate of the center of the sprite
    """

    # Init method (abstract)
    @abstractmethod
    def __init__(self, startx, starty, specific_enemy):
        """The Class Constructor.

        Args:
            self (Enemy): an instance of an enemy

            startx (integer): the starting x position of the enemy (x coordinate of spawn point)
            starty (integer): the starting y position of the enemy (y coordinate of spawn point)

            specific_enemy (integer): a number designating which specific enemy to have appear
        """
        self.enemy_health = 18
        self._enemy_move_speed = 5 # autonomous movement
        #self.velocity = [-5, self._enemy_move_speed]
        self._enemy_attacking_move_speed = 8 #slightly faster when player is noticed
       
        
        # -----Enemy Image to Load -----

        #Blue Alien
        if specific_enemy == 1:
            self._enemy_sprite = super().__init__(constants.BLUE_ALIEN, constants.CHARACTER_SCALING/2) 

        #Purple Slime
        elif specific_enemy == 2:
            self._enemy_sprite = super().__init__(constants.PURPLE_SLIME, constants.CHARACTER_SCALING/2)

        # ------------------------------


        # Where the enemy spawns; x, y coordinates
        self.center_x = startx
        self.center_y = starty


    # What an enemy does before attacking; general movement
    @abstractmethod
    def enemy_movement_auto(self):
        """Controls enemy movement before any attack is triggered; autonomous movement. Can be overrided to have none, and only target player the entire time.
        All Enemy classes must have this method present.
        
        Args:
            self (Enemy): an instance of an enemy
        """
        pass
    
    # What causes enemy to attack
    @abstractmethod
    def enemy_attack_triggering_event(self):
        """Controls the cause of enemy attack. All Enemy classes must have this method present. 

        Args:
            self (Enemy): an instance of an enemy
        """
        pass

    #Enemy attacking!
    @abstractmethod
    def enemy_attacking():
        """Controls how an enemy attacks. All Enemy classes must have this method present.
        
        Args:
            self (Enemy): an instance of an enemy
        """




# Define enemy subclasses below
class BlueAlien(Enemy):
    """A code template for a Blue Alien Enemy"""

    def __init__(self, startx, starty, specific_enemy):
        super().__init__(startx, starty, specific_enemy)
        
        
    
    # Overrides abstract method
    def enemy_movement_auto(self):
        self.change_x = -5
        self.boundary_right = int(self.center_x + (-1 * self.change_x))
        self.boundary_left = int(self.center_x + self.change_x)

        facing_right = False
        count = 0
        while True:
        
            while not facing_right:  #facing left (starting direction)
                if count == 0:
                    self.center_x += self.change_x #move left <--
                    count += 1
                else:
                    self.center_x += (self.change_x * 2)
                player_not_detected = self.enemy_attack_triggering_event() # check for player
                if not player_not_detected: 
                    break
                facing_right = True
                while facing_right:
                    self.center_x -= (self.change_x * 2) #move right -->
                    player_not_detected = self.enemy_attack_triggering_event() # check for player
                    if not player_not_detected: 
                        break
                    facing_right = False
            break
            
        
        #player detected!
        #  ...
        
        self.enemy_attacking()
        
        
    # Overrides second abstract method
    def enemy_attack_triggering_event(self):
        #Vicinity-based
        # if get_distance_between_sprites(self, director.GameView.player_sprite) < 10.0: #this doesn't work yet
        #     return False
        # else:
        #     return True
        pass
        
        
        
    #Overrides third abstract method
    def enemy_attacking(self):
        print("Enemy Attack!! Charge!")
        #Run toward player!

    

class PurpleSlime(Enemy):
    """A code template for an insect enemy that clings to platforms. Pre-programmed to walk in a certain direction and not react to player.""" 

    def __init__(self, startx, starty, specific_enemy):
        super().__init__(startx, starty, specific_enemy)
        self.enemy_health = 12 # not as much health as other enemies
        


    # Overrides abstract method
    def enemy_movement_auto(self):
        self.center_x -= 2
        

    # Overrides second abstract method
    def enemy_attack_triggering_event(self):
        # print("there is no triggering event for this enemy; they simply move in a repeatable pattern")
        pass

    # Overrides third abstract method
    def enemy_attacking(self):
        pass



# class FloatingEnemy(Enemy):
#     # A code template for a floating type of enemy.
#     # Overrides second abstract method
#     def enemy_movement_auto(self):
#         # print("I will usually simply move around in a mostly horizontal fashion, slightly floating up and down, levitating in the air.")
#         pass

#     # Overrides abstract method
#     def enemy_attack_triggering_event(self):
#         # print("\nBut I gravitate towards players as they approach me and/or start to shoot beams their way (Vicinity-based)\n")
#         pass

    
# class DeathWorm(Enemy):
#     # A code template for a Death Worm enemy. Simply moves up and down, and does not react to player.

#     def __init__(self):
#         super().__init__() # This enemy cannot be hurt
#         self._enemy_health = -1
#         if self._enemy_health == -1:
#             # print("Enemy cannot be hurt. Only an obstacle.")
#             pass

#     # Overrides second abstract method
#     def enemy_movement_auto(self):
#         # print("I move up and down, simply as a sort of obstacle.")
#         pass

#     # Overrides abstract method
#     def enemy_attack_triggering_event(self):
#         # print("\nI have no triggering event.\n")
#         pass
    

# class InsectEnemy(Enemy):
#     # A code template for an insect enemy that clings to platforms. Pre-programmed to walk in a certain direction and not react to player. 

#     def __init__(self):
#         super().__init__()
#         self._enemy_health = 10 # not as much health as other enemies

#     # Overrides second abstract method
#     def enemy_movement_auto(self):
#         # print("I walk around, cling to platforms, and to edges/walls.")
#         pass

#     # Overrides abstract method
#     def enemy_attack_triggering_event(self):
#         # print("there is no triggering event for this enemy; they simply move in a repeatable pattern")
#         pass


# class LaserShooterEnemy(Enemy):
#     # A code template for an enemy that hangs from the bottom of a platform and shoots at the player.
#     # Keeps track of player position and targets them with shots.

#     def __init__(self):
#         super().__init__()
#         self._enemy_move_speed = 0 # this enemy does not move anywhere
#         self._angle = 45
        
#     # Overrides second abstract method
#     def enemy_movement_auto(self):
#         # print("I do not move anywhere; stays in one spot.")
#         pass

#     # Overrides abstract method
#     def enemy_attack_triggering_event(self):
#         # print("If the player gets close enough, which still can be a little far off, I will shoot at them.")
#         pass
