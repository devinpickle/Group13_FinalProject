import arcade
from game import constants
from game.director import Director
from game.player import Player
from game.ground import Ground

director = Director()
director.setup()
arcade.run()