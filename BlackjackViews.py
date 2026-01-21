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
        self.table = arcade.load_texture('game_images/table.png')
        self.coins = 1000

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout.center_y += 350
        self.anchor_layout.center_x += 380

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text=f'{self.coins}',
                        font_size=30,
                        text_color=arcade.color.BLACK,
                        width=400)
        self.anchor_layout.add(label)
        music_volume = UITextureButton(text='Громкость + 1',
                                       width=150,
                                       height=50,
                                       texture=arcade.make_soft_square_texture(100, arcade.color.LIGHT_BLUE, 255, 255))
        music_volume.on_click = self.loudly
        self.anchor_layout.add(music_volume)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.table, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                              self.height))
        self.manager.draw()

    def loudly(self, event):
        pass
        # self.back_music.volume -= 0.05
        # print(self.back_music.volume)


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
