import random

import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UITextureButton, UIMessageBox
from birdGameObjects import Bird, Earth, Colon, Finish, Cloud


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
        continue_label = UILabel(text='Чтобы продолжить, нажмите ESC',
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
            return True


class GameView(arcade.View):
    def __init__(self, hardness):
        super().__init__()

        self.hardness = hardness
        self.result = 0
        self.jump_pressed = False
        self.finish_spawned = False

        self.bird_list = arcade.SpriteList()
        self.earth_list = arcade.SpriteList()
        self.colons_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()

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

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y = self.height // 2 - 50
        self.anchor_layout.center_x = self.width // 2 - 950

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        self.label = UILabel(text=f'Счёт: {self.result}',
                             font_size=20,
                             text_color=arcade.color.BLACK,
                             width=400,
                             align='center'
                             )
        self.box_layout.add(self.label)

    def on_update(self, delta_time):
        if len(self.clouds_list) < 6:
            cloud = Cloud()
            self.clouds_list.append(cloud)
        self.clouds_list.update(delta_time)
        bird_collisions_with_colons = arcade.check_for_collision_with_list(self.bird, self.colons_list)
        bird_collisions_with_earth = arcade.check_for_collision_with_list(self.bird, self.earth_list)
        if bird_collisions_with_earth or bird_collisions_with_colons or self.bird.center_y >= self.height:
            self.game_over()
            return True

        for colon in self.colons_list:
            if colon.center_x <= 25:
                self.result += 0.5
                colon.remove_from_sprite_lists()
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

        if self.jump_pressed:
            self.engine.jump(6)

        if self.finish_list:
            bird_finished = arcade.check_for_collision_with_list(self.bird, self.finish_list)
            if bird_finished or self.bird.center_x >= self.finish.center_x:
                self.win()
                return True
        if self.finish_spawned and not self.finish_list:
            self.finish = Finish()
            self.finish.center_x = 920
            self.finish.center_y = 300
            self.finish_list.append(self.finish)
        if self.finish_spawned and not self.colons_list:
            self.bird.move = True
        self.colons_list.update()
        self.bird_list.update(delta_time)

        self.engine.update()
        result = int(self.result)
        self.label.text = f'Счёт: {result}'
        if result == 16 and self.hardness == 'easy':
            self.finish_spawned = True
        elif result == 46 and self.hardness == 'medium':
            self.finish_spawned = True
        elif result == 146 and self.hardness == 'easy':
            self.finish_spawned = True

    def on_draw(self):
        self.clear()
        self.background_color = arcade.color.LIGHT_BLUE
        self.clouds_list.draw()
        self.colons_list.draw()
        self.finish_list.draw()
        self.bird_list.draw()
        self.earth_list.draw()
        self.manager.draw()

    def on_key_press(self, key, modifier):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.SPACE:
            self.jump_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.jump_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.jump_pressed = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.jump_pressed = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.jump_pressed = False
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.jump_pressed = False

    def game_over(self):
        game_over_view = GameOverView(self.hardness)
        self.window.show_view(game_over_view)

    def win(self):
        win = WinView(self.hardness)
        self.window.show_view(win)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.buttons_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y += self.height // 4

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.box_layout.add(self.buttons_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text='Выберите Уровень сложности',
                               font_size=20,
                               text_color=arcade.color.BLACK,
                               width=400,
                               align='center')
        easy_button = UITextureButton(text='Лёгкий',
                                         width=150,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                         )
        easy_button.on_click = self.easy
        medium_button = UITextureButton(text='Средний',
                                      width=150,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                      )
        medium_button.on_click = self.medium
        hard_button = UITextureButton(text='Сложный',
                                      width=150,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        hard_button.on_click = self.hard
        infinity_button = UITextureButton(text='Бесконечный',
                                      width=150,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        infinity_button.on_click = self.infinity
        self.box_layout.add(label)
        self.buttons_layout.add(easy_button)
        self.buttons_layout.add(medium_button)
        self.buttons_layout.add(hard_button)
        self.buttons_layout.add(infinity_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def easy(self, event):
        game = GameView('easy')
        self.window.show_view(game)

    def medium(self, event):
        game = GameView('medium')
        self.window.show_view(game)

    def hard(self, event):
        game = GameView('hard')
        self.window.show_view(game)

    def infinity(self, event):
        game = GameView('infinity')
        self.window.show_view(game)

    def on_hide_view(self):
        self.manager.disable()


class WinView(arcade.View):
    def __init__(self, hardness):
        super().__init__()
        self.background_color = arcade.color.LIGHT_BLUE

        self.hardness = hardness

        self.bird_list = arcade.SpriteList()
        bird = Bird(win=True)
        bird.center_x = self.width // 2
        bird.center_y = 3 * self.height // 4
        self.bird_list.append(bird)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.box_layout.add(self.buttons_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text='Победа!',
                        font_size=20,
                        text_color=arcade.color.BLACK,
                        width=400,
                        align='center')
        second_label = UILabel(text='Нажмите на кнопки ниже, или клавиши, соответсвующие этим кнопкам',
                               font_size=20,
                               text_color=arcade.color.BLACK,
                               width=400,
                               align='center')
        restart_button = UITextureButton(text='Начать Заново (R)',
                                         width=150,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                         )
        restart_button.on_click = self.restart
        menu_button = UITextureButton(text='Меню (Enter)',
                                      width=100,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                      )
        menu_button.on_click = self.menu
        exit_button = UITextureButton(text='Выйти (ESC)',
                                      width=100,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        exit_button.on_click = self.exit
        self.box_layout.add(label)
        self.box_layout.add(second_label)
        self.buttons_layout.add(restart_button)
        self.buttons_layout.add(menu_button)
        self.buttons_layout.add(exit_button)

    def on_draw(self):
        self.clear()
        self.bird_list.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.restart('Key')
        elif key == arcade.key.ENTER:
            self.menu('Key')
        elif key == arcade.key.ESCAPE:
            self.exit('Key')

    def restart(self, event):
        game_view = GameView(self.hardness)
        self.window.show_view(game_view)

    def menu(self, event):
        menu = MenuView()
        self.window.show_view(menu)

    def exit(self, event):
        message_box = UIMessageBox(message_text='Вы действительно хотите выйти?',
                                   width=400,
                                   height=200,
                                   buttons=('Да', 'Нет'))
        message_box.on_action = self.on_message_box
        self.manager.add(message_box)

    def on_message_box(self, button_text):
        if button_text.action == 'Да':
            arcade.Window.close(self.window)
        else:
            game_over = WinView(self.hardness)
            self.window.show_view(game_over)

    def on_hide_view(self):
        self.manager.disable()


class GameOverView(arcade.View):
    def __init__(self, hardness):
        super().__init__()
        self.background_color = arcade.color.LIGHT_BLUE

        self.hardness = hardness

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.box_layout.add(self.buttons_layout)
        self.manager.add(self.anchor_layout)

        self.bird_list = arcade.SpriteList()
        bird = Bird(lose=True)
        bird.center_x = self.width // 2
        bird.center_y = 3 * self.height // 4
        self.bird_list.append(bird)

    def setup_widgets(self):
        label = UILabel(text='Поражение!',
                        font_size=20,
                        text_color=arcade.color.BLACK,
                        width=400,
                        align='center')
        self.box_layout.add(label)
        second_label = UILabel(text='Нажмите на кнопки ниже, или клавиши, соответсвующие этим кнопкам',
                               font_size=20,
                               text_color=arcade.color.BLACK,
                               width=400,
                               align='center')
        restart_button = UITextureButton(text='Начать Заново (R)',
                                         width=150,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                         )
        restart_button.on_click = self.restart
        menu_button = UITextureButton(text='Меню (Enter)',
                                      width=100,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                      )
        menu_button.on_click = self.menu
        exit_button = UITextureButton(text='Выйти (ESC)',
                                      width=100,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        exit_button.on_click = self.exit
        self.box_layout.add(label)
        self.box_layout.add(second_label)
        self.buttons_layout.add(restart_button)
        self.buttons_layout.add(menu_button)
        self.buttons_layout.add(exit_button)

    def on_draw(self):
        self.clear()
        self.bird_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.restart('Key')
        elif key == arcade.key.ENTER:
            self.menu('Key')
        elif key == arcade.key.ESCAPE:
            self.exit('Key')

    def restart(self, event):
        game_view = GameView(self.hardness)
        self.window.show_view(game_view)

    def menu(self, event):
        menu = MenuView()
        self.window.show_view(menu)

    def exit(self, event):
        message_box = UIMessageBox(message_text='Вы действительно хотите выйти?',
                                   width=400,
                                   height=200,
                                   buttons=('Да', 'Нет'))
        message_box.on_action = self.on_message_box
        self.manager.add(message_box)

    def on_message_box(self, button_text):
        if button_text.action == 'Да':
            arcade.Window.close(self.window)
        else:
            game_over = GameOverView(self.hardness)
            self.window.show_view(game_over)

    def on_hide_view(self):
        self.manager.disable()