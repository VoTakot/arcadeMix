import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UITextureButton, UIInputText, UILabel, UISlider

VOLUME = 0.25


def change_volume(event):
    global VOLUME
    VOLUME = float(event.new_value / 100)
    print(VOLUME)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.RED_DEVIL

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        play_btn = UITextureButton(text='Начать',
                                   width=150,
                                   height=50,
                                   texture=arcade.make_soft_square_texture(100, arcade.color.LIGHT_BLUE, 255, 255)
                                   )
        play_btn.on_click = self.start
        settings_btn = UITextureButton(text='Настройки',
                                       width=150,
                                       height=50,
                                       texture=arcade.make_soft_square_texture(100, arcade.color.LIGHT_BLUE, 255, 255))
        settings_btn.on_click = self.open_settings
        self.box_layout.add(play_btn)
        self.box_layout.add(settings_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def start(self, event):
        game_view = GameView()
        self.window.show_view(game_view)

    def open_settings(self, event):
        settings_view = SettingsView(self)
        self.window.show_view(settings_view)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # music = arcade.load_sound('sounds/music.mp3')
        # self.back_music = arcade.play_sound(music, loop=True, volume=0.2)
        self.bet_done = False
        self.bet = 0
        self.coins = 10

        self.table = arcade.load_texture('game_images/table.png')

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y += 350
        self.anchor_layout.center_x += 380

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.label = UILabel()

    def setup_widgets(self):
        self.label = UILabel(text=f'{self.coins}',
                             font_size=30,
                             text_color=arcade.color.BLACK,
                             width=400)
        self.box_layout.add(self.label)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.table, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                              self.height))
        self.manager.draw()

    def on_update(self, delta_time):
        if not self.coins and not self.bet:
            view = GameOver()
            self.window.show_view(view)
        if not self.bet_done:
            view = BetView(self, self.coins)
            self.window.show_view(view)
            return True
        self.label.text = f'{self.coins}'


class BetView(arcade.View):
    def __init__(self, view, money=0):
        super().__init__()
        self.view = view
        self.money = money
        self.bet = 0

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=10)
        self.bet_value = None

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        delete_five_hundred = UITextureButton(text='-500',
                                              width=50,
                                              height=50,
                                              texture=arcade.make_soft_square_texture(100, arcade.color.RED, 255, 255))
        delete_five_hundred.on_click = self.sub_five_hundred

        delete_quarter = UITextureButton(text='-250',
                                         width=50,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.RED, 255, 255))
        delete_quarter.on_click = self.sub_quarter

        delete_hundred = UITextureButton(text='-100',
                                         width=50,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.RED, 255, 255))
        delete_hundred.on_click = self.sub_hundred

        clear_bet = UITextureButton(text='0',
                                    width=50,
                                    height=50,
                                    texture=arcade.make_soft_square_texture(100, arcade.color.DARK_GRAY, 255, 255))
        clear_bet.on_click = self.clear_bet

        add_hundred = UITextureButton(text='+100',
                                      width=50,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.GREEN, 255, 255))
        add_hundred.on_click = self.add_hundred

        add_quarter = UITextureButton(text='+250',
                                      width=50,
                                      height=50,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.GREEN, 255, 255))
        add_quarter.on_click = self.add_quarter

        add_five_hundred = UITextureButton(text='+500',
                                           width=50,
                                           height=50,
                                           texture=arcade.make_soft_square_texture(100, arcade.color.GREEN, 255, 255))
        add_five_hundred.on_click = self.add_five_hundred

        label = UILabel(text='Ставка',
                        font_size=30,
                        text_color=arcade.color.BLACK,
                        width=400,
                        align='center')
        self.box_layout.add(label)

        second_label = UILabel(text='Выберете сумму ставки',
                               font_size=25,
                               text_color=arcade.color.BLACK,
                               width=400,
                               align='center'
                               )
        self.box_layout.add(second_label)

        third_label = UILabel(
            text='!Внимание, в случае проигрыша, вы можете потерять всю сумму ставки и закончить игру!',
            font_size=11,
            text_color=arcade.color.RED,
            width=400,
            align='center')
        self.box_layout.add(third_label)

        self.bet_value = UIInputText(width=200, height=50, text_color=arcade.color.BLACK)
        self.bet_value.on_change = self.set_bet
        self.box_layout.add(self.bet_value)

        accept_btn = UITextureButton(text='Принять', width=80, height=50,
                                     texture=arcade.make_soft_square_texture(100, arcade.color.GREEN, 255, 255))
        accept_btn.on_click = self.save_bet

        self.buttons_layout.add(delete_five_hundred)
        self.buttons_layout.add(delete_quarter)
        self.buttons_layout.add(delete_hundred)
        self.buttons_layout.add(clear_bet)
        self.buttons_layout.add(add_hundred)
        self.buttons_layout.add(add_quarter)
        self.buttons_layout.add(add_five_hundred)

        self.box_layout.add(self.buttons_layout)
        self.box_layout.add(accept_btn)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 5, self.height // 5, self.width - 2 * self.width // 5,
                                          self.height - 2 * self.height // 5, arcade.color.LIGHT_GRAY)
        self.manager.draw()

    def sub_five_hundred(self, event):
        self.bet -= 500
        if self.bet < 0:
            self.bet = 0
        self.bet_value.text = str(self.bet)

    def sub_quarter(self, event):
        self.bet -= 250
        if self.bet < 0:
            self.bet = 0
        self.bet_value.text = str(self.bet)

    def sub_hundred(self, event):
        self.bet -= 100
        if self.bet < 0:
            self.bet = 0
        self.bet_value.text = str(self.bet)

    def clear_bet(self, event):
        self.bet = 0
        self.bet_value.text = str(self.bet)

    def set_bet(self, event):
        if int(event.new_value) > self.money:
            self.bet_value.text = str(self.money)
        elif int(event.new_value) < 0:
            self.bet_value.text = '0'
        self.bet = int(event.new_value)

    def add_hundred(self, event):
        self.bet += 100
        if self.bet > self.money:
            self.bet -= self.bet - self.money
        self.bet_value.text = str(self.bet)

    def add_quarter(self, event):
        self.bet += 250
        if self.bet > self.money:
            self.bet -= self.bet - self.money
        self.bet_value.text = str(self.bet)

    def add_five_hundred(self, event):
        self.bet += 500
        if self.bet > self.money:
            self.bet -= self.bet - self.money
        self.bet_value.text = str(self.bet)

    def save_bet(self, event):
        if self.bet:
            self.view.bet_done = True
            self.view.bet = self.bet
            self.view.coins -= self.bet
            self.window.show_view(self.view)
            return True


class SettingsView(arcade.View):
    def __init__(self, view: arcade.View):
        super().__init__()

        self.view = view

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y += 100

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        slider = UISlider(min_value=0, max_value=100, step=1, value=25)
        slider.on_change = change_volume
        self.box_layout.add(slider)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 4, self.height // 4, self.width // 2, self.height // 2,
                                          arcade.color.GRAY)
        self.manager.draw()

    def return_back(self):
        self.window.show_view(self.view)


class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN
        homeless = arcade.Sprite('game_images/homeless.png', 8)
        homeless.center_x = 3 * self.width // 4
        homeless.center_y = self.height // 2
        self.homeless_list = arcade.SpriteList()
        self.homeless_list.append(homeless)

    def on_draw(self):
        self.clear()
        self.homeless_list.draw()
