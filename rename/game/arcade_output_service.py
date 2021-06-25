import sys
import arcade

class ArcadeOutputService:


    def __init__(self):
        """Class constructor"""

        pass

    def clear_screen(self):
        arcade.start_render()

    def draw_actor(self, actor):
        actor.draw()

    def draw_actors(self, actors):
        for actor in actors:
            self.draw_actor(actor)