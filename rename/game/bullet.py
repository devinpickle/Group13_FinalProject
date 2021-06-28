from game import constants
import arcade

class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(constants.GROUND_IMAGE, 0.3)

        self.center_x = x
        self.center_y = y

        self.change_x = constants.BULLET_SPEED