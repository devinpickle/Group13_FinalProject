import arcade
from game.director import Director
from game import constants

class MenuView(arcade.View):
    
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, "Jumping Bullets")
        director = Director()
        director.setup()
        window.show_view(director)
        arcade.run()