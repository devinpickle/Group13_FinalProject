from abc import ABC, abstractmethod
import arcade

class Enemy(arcade.Sprite, ABC):
    """A code template for the basic functionality of enemies in-game. Responsible for controlling enemy health, and so on.
    
    Stereotype:
        Coordinator, Information Holder
    
    Attributes:
        _enemy_health (integer): the amount of health an enemy has
        _enemy_move_speed (integer): the speed of enemy movement
    """

    # Init method
    def __init__(self):
        """The Class Constructor.

        Args:
            self (Enemy): an instance of an enemy
        """
        self._enemy_health = 50
        self._enemy_move_speed = 5 # autonomous movement; speed set to 5
    
    # What causes enemy to attack
    @abstractmethod
    def enemy_attack_triggering_event(self):
        """Controls the cause of enemy attack. All Enemy classes must have this method present. 

        Args:
            self (Enemy): an instance of an enemy
        """
        pass
    
    # What an enemy does before attacking; general movement
    @abstractmethod
    def enemy_movement_auto(self):
        """Controls enemy movement before any attack is triggered; autonomous movement. Can be overrided to have none, and only target player the entire time.
        All Enemy classes must have this method present.
        
        Args:
            self (Enemy): an instance of an enemy
        """
        pass




# Define enemy subclasses below
class FloatingEnemy(Enemy):
    # A code template for a floating type of enemy.
    # Overrides second abstract method
    def enemy_movement_auto(self):
        # print("I will usually simply move around in a mostly horizontal fashion, slightly floating up and down, levitating in the air.")
        pass

    # Overrides abstract method
    def enemy_attack_triggering_event(self):
        # print("\nBut I gravitate towards players as they approach me and/or start to shoot beams their way (Vicinity-based)\n")
        pass

    
class DeathWorm(Enemy):
    # A code template for a Death Worm enemy. Simply moves up and down, and does not react to player.

    def __init__(self):
        super().__init__() # This enemy cannot be hurt
        self._enemy_health = -1
        if self._enemy_health == -1:
            # print("Enemy cannot be hurt. Only an obstacle.")
            pass

    # Overrides second abstract method
    def enemy_movement_auto(self):
        # print("I move up and down, simply as a sort of obstacle.")
        pass

    # Overrides abstract method
    def enemy_attack_triggering_event(self):
        # print("\nI have no triggering event.\n")
        pass
    

class InsectEnemy(Enemy):
    # A code template for an insect enemy that clings to platforms. Pre-programmed to walk in a certain direction and not react to player. 

    def __init__(self):
        super().__init__()
        self._enemy_health = 10 # not as much health as other enemies

    # Overrides second abstract method
    def enemy_movement_auto(self):
        # print("I walk around, cling to platforms, and to edges/walls.")
        pass

    # Overrides abstract method
    def enemy_attack_triggering_event(self):
        # print("there is no triggering event for this enemy; they simply move in a repeatable pattern")
        pass


class LaserShooterEnemy(Enemy):
    # A code template for an enemy that hangs from the bottom of a platform and shoots at the player.
    # Keeps track of player position and targets them with shots.

    def __init__(self):
        super().__init__()
        self._enemy_move_speed = 0 # this enemy does not move anywhere
        self._angle = 45
        
    # Overrides second abstract method
    def enemy_movement_auto(self):
        # print("I do not move anywhere; stays in one spot.")
        pass

    # Overrides abstract method
    def enemy_attack_triggering_event(self):
        # print("If the player gets close enough, which still can be a little far off, I will shoot at them.")
        pass

# code to test classes are working properly (with print statements active)
# ghastly_beam_shooter = FloatingEnemy()
# ghastly_beam_shooter.enemy_movement_auto()
# ghastly_beam_shooter.enemy_attack_triggering_event()

# print()

# death_worm = DeathWorm()
# death_worm.enemy_movement_auto()
# death_worm.enemy_attack_triggering_event()

# enemy_insect = InsectEnemy()
# enemy_insect.enemy_movement_auto()
# enemy_insect.enemy_attack_triggering_event()

# deadly_shooter = LaserShooterEnemy()
# print(deadly_shooter.angle)