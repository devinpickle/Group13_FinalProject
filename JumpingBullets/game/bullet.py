import arcade

class Bullet(arcade.SpriteSolidColor):
    # Bullet sprite
        
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        
        if self.center_y < -100:
            self.remove_from_sprite_lists()
        


        # How far a bullet can travel before disappearing
        # self.start = x
        # self.distance = 300
        # self.bullet_travel_right = self.start + self.distance
        # self.bullet_travel_left = self.start - self.distance