import random

import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIMessageBox
from birdGameObjects import Bird, Earth, Colon, Finish


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.batch = Batch()

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y += 100

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        pause_label = UILabel(text='Пауза!',
                              width=800,
                              height=100,
                              font_size=30,
                              text_color=arcade.color.BLACK,
                              )
        continue_label = UILabel(text='Чnобы продолжить, нажмите ESC',
                                 width=800,
                                 height=100,
                                 font_size=30,
                                 text_color=arcade.color.BLACK,
                                 )

        self.box_layout.add(pause_label)
        self.box_layout.add(continue_label)

    def on_draw(self):
        self.clear()
        self.background_color = arcade.color.LIGHT_BLUE
        arcade.draw_polygon_filled([[100, 100], [100, 500], [900, 500], [900, 100]], color=arcade.color.WHITE)
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.result = 0
        self.jump_pressed = False
        self.finish_spawned = False

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()
        self.bird_list = arcade.SpriteList()
        self.earth_list = arcade.SpriteList()
        self.colons_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.bird = Bird()
        self.bird.center_x = 100
        self.bird.center_y = self.height // 2
        self.bird_list.append(self.bird)
        for i in range(int(self.width) // 100 + 1):
            earth = Earth()
            earth.center_x = 100 * i
            earth.center_y = 50
            self.earth_list.append(earth)
        self.last_colon = 0
        self.first_colon = 0

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.bird,
            gravity_constant=0.45
        )

    def setup_widgets(self):
        pass

    def on_update(self, delta_time):
        self.colons_list.update(delta_time)
        if (not self.colons_list or self.last_colon.center_x <= 750) and not self.finish_spawned:
            up_colon = Colon('up')
            bottom_colon = Colon('bottom')
            up_colon.center_x = 975
            up_colon.center_y = random.randint(450, 700)
            bottom_colon.center_x = 975
            bottom_colon.center_y = up_colon.center_y - 600
            self.last_colon = up_colon
            self.colons_list.append(up_colon)
            self.colons_list.append(bottom_colon)
        if self.finish_spawned:
            finish = Finish()
            finish.center_x = 920
            finish.center_y = 300
            self.finish_list.append(finish)
        if self.finish_spawned and not self.colons_list:
            self.bird.update(delta_time)
        if self.jump_pressed:
            self.engine.jump(6)
        if self.finish_list:
            bird_finished = arcade.check_for_collision_with_list(self.bird, self.finish_list)
            if bird_finished:
                win_view = WinView()
                self.window.show_view(win_view)
        self.engine.update()
        if self.colons_list:
            bird_collisions = arcade.check_for_collision_with_list(self.bird, self.colons_list) or\
                              arcade.check_for_collision_with_list(self.bird, self.earth_list)
            if bird_collisions:
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            for colon in self.colons_list:
                if colon.center_x <= 25:
                    colon.remove_from_sprite_lists()
                    self.result += 0.5
        result = int(self.result)
        if result == 1:
            self.finish_spawned = True
        print(result)


    def on_draw(self):
        self.clear()
        self.background_color = arcade.color.LIGHT_BLUE
        self.colons_list.draw()
        self.finish_list.draw()
        self.bird_list.draw()
        self.earth_list.draw()

    def on_key_press(self, key, modifier):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.SPACE:
            self.jump_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.jump_pressed = False


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY  # Фон для меню

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", self.window.width / 2, self.window.height / 2 + 50,
                                     arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми ESC, чтобы начать!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameView()
            self.window.show_view(game_view)


class WinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            menu_view = MenuView()
            self.window.show_view(menu_view)
        elif key == arcade.key.ESCAPE:
            arcade.Window.close(self.window)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            menu_view = MenuView()
            self.window.show_view(menu_view)
        elif key == arcade.key.ESCAPE:
            arcade.Window.close(self.window)
