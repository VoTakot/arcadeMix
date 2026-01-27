import arcade
from arcade.gui import UIManager, UIFlatButton, UIAnchorLayout, UIBoxLayout

import GameScenes
import BlackjackViews
import SnakeGame
import GemThreeGame


class StartWindowView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.WHITE

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.top_buttons_layout = UIBoxLayout(vertical=False, space_between=10)
        self.bottom_buttons_layout = UIBoxLayout(vertical=False, space_between=10)

        self.box_layout.add(self.top_buttons_layout)
        self.box_layout.add(self.bottom_buttons_layout)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        flappy_bird_btn = UIFlatButton(text='Flappy Bird',
                                       width=245,
                                       height=195)
        flappy_bird_btn.on_click = self.start_flappy
        self.top_buttons_layout.add(flappy_bird_btn)

        blackjack_btn = UIFlatButton(text='Блекджек',
                                     width=245,
                                     height=195)
        blackjack_btn.on_click = self.start_blackjack
        self.top_buttons_layout.add(blackjack_btn)

        snake_btn = UIFlatButton(text='Змейка',
                                 width=245,
                                 height=195)
        snake_btn.on_click = self.start_snake
        self.bottom_buttons_layout.add(snake_btn)

        gem_three_btn = UIFlatButton(text='Три в ряд',
                                     width=245,
                                     height=195)
        gem_three_btn.on_click = self.start_gem_three
        self.bottom_buttons_layout.add(gem_three_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_texture_rect(texture=arcade.load_texture('game_icons/flappybird.png'),
                                 rect=arcade.Rect(x=125,
                                                  y=405,
                                                  width=200,
                                                  height=200,
                                                  bottom=500,
                                                  left=0,
                                                  top=600,
                                                  right=100))
        arcade.draw_texture_rect(texture=arcade.load_texture('game_icons/snake.png'),
                                 rect=arcade.Rect(x=125,
                                                  y=200,
                                                  width=200,
                                                  height=200,
                                                  bottom=500,
                                                  left=0,
                                                  top=600,
                                                  right=100))
        arcade.draw_texture_rect(texture=arcade.load_texture('game_icons/blackjack.png'),
                                 rect=arcade.Rect(x=855,
                                                  y=405,
                                                  width=200,
                                                  height=200,
                                                  bottom=500,
                                                  left=0,
                                                  top=600,
                                                  right=100))
        arcade.draw_texture_rect(texture=arcade.load_texture('game_icons/GemThree.png'),
                                 rect=arcade.Rect(x=855,
                                                  y=200,
                                                  width=200,
                                                  height=200,
                                                  bottom=500,
                                                  left=0,
                                                  top=600,
                                                  right=100))

    def start_flappy(self, event):
        view = GameScenes.MenuView()
        self.window.show_view(view)

    def start_blackjack(self, event):
        view = BlackjackViews.MenuView()
        self.window.height = 800
        self.window.show_view(view)

    def start_snake(self, event):
        arcade.Window.close(self.window)
        SnakeGame.main()

    def start_gem_three(self, event):
        arcade.Window.close(self.window)
        GemThreeGame.main()

    def on_hide_view(self):
        self.manager.disable()


if __name__ == '__main__':
    window = arcade.Window(title='ArcadeMix', width=1000, height=600)
    main_view = StartWindowView()
    window.show_view(main_view)
    arcade.run()
