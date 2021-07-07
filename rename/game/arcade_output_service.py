import sys, arcade

class ArcadeOutputService:
    """Renders and draws screen with actors. Capable of clearing the screen, and updating it with new actor positions.

    Stereotype:
        Service Provider
    
    Attributes:
        none
    """
    def __init__(self):
        # Class constructor
        pass

    def clear_screen(self):
        """Starts rendering of screen.
        
        Args:
            self (ArcadeOutputService): an instance of ArcadeOutputService
        """
        arcade.start_render()

    def draw_actor(self, actor):
        """Draws on actor on the screen. 

        Args: 
            self (ArcadeOutputService): an instance of ArcadeOutputService
            actor (Sprite): an instance of a sprite
        """
        actor.draw()

    def draw_actors(self, actors):
        """Draws multiple actors on the screen. 

        Args:
            self (ArcadeOutputService): an instance of ArcadeOutputService
            actors (Sprites): instances of multiple sprites
        """
        for actor in actors:
            self.draw_actor(actor)