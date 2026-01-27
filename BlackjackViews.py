import random

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UITextureButton, UIInputText, UILabel, UISlider, \
    UIMessageBox
from BlackjackObjects import Card, Hand

VOLUME = 0.25
CARDS_NUMBERS = list(range(1, 53))


def change_volume(event):
    global VOLUME
    VOLUME = float(event.new_value / 100)


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
        music = arcade.load_sound('sounds/music2.mp3')
        self.back_music = arcade.play_sound(music, loop=True, volume=VOLUME)
        self.bet_done = False
        self.bet = 0
        self.coins = 1000
        self.first_bet = 0
        self.insurance_bet = 0
        self.insurance_bet_done = False
        self.final = False

        self.cards_list = arcade.SpriteList()
        self.player_cards = 0
        self.dealer_cards = 0
        self.player_points = 0
        self.dealer_points = 0

        self.dealers_new_card = False
        self.new_card = True
        self.player_takes_card = False
        self.need_card = False

        self.buttons_added = False

        self.cards_remaining = CARDS_NUMBERS.copy()

        self.table = arcade.load_texture('game_images/table.png')

        self.hand = Hand('player', self.player_cards)
        self.hand.center_x = 210
        self.hand.center_y = 1200
        self.hand_list = arcade.SpriteList()
        self.hand_list.append(self.hand)

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
        self.label = UILabel(text=f'{self.coins}',
                             font_size=30,
                             text_color=arcade.color.BLACK,
                             width=400,
                             x=802,
                             y=725)
        self.bet_label = UILabel(text=f'{self.bet}',
                                 font_size=30,
                                 text_color=arcade.color.BLACK,
                                 width=400,
                                 x=802,
                                 y=653
                                 )
        self.add_card_btn = UITextureButton(texture=arcade.load_texture('game_images/plus_card.png'),
                                            width=106,
                                            height=107,
                                            y=190,
                                            x=395 + 120 * (self.player_cards - 2)
                                            )
        self.add_card_btn.on_click = self.taking_card
        self.accept_cards_btn = UITextureButton(texture=arcade.load_texture('game_images/accept_cards.png'),
                                                width=106,
                                                height=107,
                                                y=190,
                                                x=870
                                                )
        self.accept_cards_btn.on_click = self.dealer_step
        self.manager.add(self.label)
        self.manager.add(self.bet_label)

    def on_update(self, delta_time):
        self.coins = int(self.coins)
        self.bet = int(self.bet)
        self.back_music.volume = VOLUME
        if self.coins == 0 and self.bet == 0:  # проверка на проигрыш
            view = GameOver()
            self.window.show_view(view)
            return False

        self.label.text = f'{int(self.coins)}'
        self.bet_label.text = f'{int(self.bet)}'

        if not self.bet_done:  # создание ставки
            view = BetView(self, self.coins)
            self.window.show_view(view)
            return True

        if self.bet == 0:  # сохранение ставки, обновление монет на экране
            self.bet = self.first_bet
            self.coins = self.coins - self.bet
            self.label.text = str(self.coins)

        if (self.player_cards < 2 or self.player_takes_card) and \
                not self.hand.going_back:  # начальные карты игрока и дилера
            self.manager.remove(self.add_card_btn)
            self.manager.remove(self.accept_cards_btn)
            self.new_card = True
            self.hand.card_owner = 'player'
            self.hand.card_number = self.player_cards
        elif (self.dealer_cards < 2 or self.dealers_new_card) and not self.hand.going_back:
            self.manager.remove(self.add_card_btn)
            self.manager.remove(self.accept_cards_btn)
            self.new_card = True
            self.new_card = True
            self.hand.card_owner = 'dealer'
            self.hand.card_number = self.dealer_cards

        if self.new_card or self.hand.going_back:  # движение руки
            self.hand_list.update()

        if self.hand.place_card:  # размещение карт на столе
            random_card = random.choice(self.cards_remaining)
            card = Card(random_card)
            self.cards_remaining.remove(random_card)
            if type(card.points) == int:
                if self.hand.card_owner == 'dealer':
                    self.dealer_points += card.points
                else:
                    self.player_points += card.points
            else:
                if self.hand.card_owner == 'dealer':
                    if self.dealer_points <= 10:
                        self.dealer_points += card.points[1]
                    else:
                        self.dealer_points += card.points[0]
                else:
                    if self.player_points <= 10:
                        self.player_points += card.points[1]
                    else:
                        self.player_points += card.points[0]
            if self.hand.card_owner == 'dealer':
                card.center_y = 481
                card.center_x = 209 + self.dealer_cards * 120
                self.dealer_cards += 1
            else:
                card.center_y = 237
                card.center_x = 209 + self.player_cards * 120
                self.player_cards += 1
            self.cards_list.append(card)
            self.hand.place_card = False
            self.new_card = False
            self.player_takes_card = False
            if self.buttons_added and not self.dealers_new_card:
                self.buttons_added = False
                self.need_card = True

        if self.dealer_cards == 1 and self.dealer_points != 11 and self.player_points == 21 and not \
                self.hand.going_back:
            self.coins += 3 * self.bet
            view = WinView(self, 3)
            self.window.show_view(view)
            return True

        if self.dealer_cards == 1 and self.dealer_points == 11 and not self.hand.going_back and \
                not self.insurance_bet_done:
            view = InsuranceView(self.coins, self.bet, self)
            self.window.show_view(view)
            return True

        if self.player_cards == 2 and self.dealer_cards == 2:
            self.need_card = True

        if self.need_card and not self.hand.going_back and not self.buttons_added:
            if self.player_cards < 6:
                self.add_card_btn.center_x = 448 + 120 * (self.player_cards - 2)
                self.manager.add(self.add_card_btn)
                self.manager.add(self.accept_cards_btn)
                self.buttons_added = True
                self.need_card = False
            else:
                self.manager.add(self.accept_cards_btn)
                self.buttons_added = True
                self.need_card = False

        if self.player_points > 21 and not self.hand.going_back:
            view = LoseView(self, 1)
            self.window.show_view(view)

        if self.dealers_new_card and self.dealer_points >= 17 and not self.hand.going_back and not self.final:
            self.dealers_new_card = False
            self.final = True
            self.count_points()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.table, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                              self.height))
        self.cards_list.draw()
        self.hand_list.draw()
        self.manager.draw()

    def restart(self):
        self.bet_done = False
        self.bet = 0
        self.first_bet = 0
        self.insurance_bet = 0
        self.insurance_bet_done = False

        self.cards_list = arcade.SpriteList()
        self.player_cards = 0
        self.dealer_cards = 0
        self.player_points = 0
        self.dealer_points = 0
        self.new_card = True
        self.buttons_added = False
        self.need_card = False
        self.final = False

        self.cards_remaining = CARDS_NUMBERS.copy()

    def taking_card(self, event):
        self.player_takes_card = True

    def dealer_step(self, event):
        self.dealers_new_card = True

    def count_points(self):
        if self.player_points == self.dealer_points:
            self.coins += self.bet
            view = WinView(self, 2)
            self.window.show_view(view)
        elif self.dealer_points > 21:
            self.coins += self.bet
            view = WinView(self, 4)
            self.window.show_view(view)
        elif self.dealer_points > self.player_points:
            view = LoseView(self, 2)
            self.window.show_view(view)
        elif self.player_points > self.dealer_points:
            self.coins += 1.5 * self.bet
            view = WinView(self, 1)
            self.window.show_view(view)
        if self.insurance_bet_done and self.dealer_points == 21:
            self.coins += 2 * self.insurance_bet

    def on_hide_view(self):
        self.manager.disable()
        self.back_music.pause()

    def on_show_view(self):
        self.manager.enable()
        self.back_music.play()


class WinView(arcade.View):
    def __init__(self, view, code):
        super().__init__()
        self.view = view
        self.code = code

        if self.code == 1:
            self.win_text = 'Вы набрали больше очков, чем дилер'
        elif self.code == 2:
            self.win_text = 'Вы набрали столько же очков, сколько и дилер'
        elif self.code == 3:
            self.win_text = 'Вы собрали блекджек!'
        elif self.code == 4:
            self.win_text = 'Дилер набрал больше 21 очка'

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=10)

        self.setup_widgets()

        self.box_layout.add(self.buttons_layout)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        win_label = UILabel(text='Победа',
                            font_size=35,
                            text_color=arcade.color.BLACK,
                            width=200,
                            align='center'
                            )
        self.box_layout.add(win_label)

        second_win_label = UILabel(text=self.win_text,
                                   font_size=20,
                                   text_color=arcade.color.BLACK,
                                   width=400,
                                   align='center'
                                   )
        self.box_layout.add(second_win_label)

        continue_button = UITextureButton(text='Продолжить',
                                          width=130,
                                          height=50,
                                          texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                          )
        continue_button.on_click = self.continue_game
        self.buttons_layout.add(continue_button)

        end_button = UITextureButton(text='Выйти',
                                     width=50,
                                     height=50,
                                     texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                     )
        end_button.on_click = self.end_game
        self.buttons_layout.add(end_button)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 5, self.height // 5, self.width - 2 * self.width // 5,
                                          self.height - 2 * self.height // 5, arcade.color.LIGHT_GRAY)
        self.manager.draw()

    def continue_game(self, event):
        self.view.restart()
        self.window.show_view(self.view)

    def end_game(self, event):
        self.message_box = UIMessageBox(message_text='Вы действительно хотите выйти?',
                                        width=400,
                                        height=200,
                                        buttons=('Да', 'Нет'))
        self.message_box.on_action = self.on_message_box
        self.manager.add(self.message_box)

    def on_message_box(self, button_text):
        if button_text.action == 'Да':
            arcade.Window.close(self.window)
        else:
            self.manager.remove(self.message_box)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


class LoseView(arcade.View):
    def __init__(self, view, code):
        super().__init__()
        self.view = view
        self.code = code

        if self.code == 1:
            self.lose_text = 'Вы превысили 21 очко'
        elif self.code == 2:
            self.lose_text = 'Вы набрали меньше очков, чем дилер'

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=10)

        self.setup_widgets()

        self.box_layout.add(self.buttons_layout)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        lose_label = UILabel(text='Поражение',
                             font_size=35,
                             text_color=arcade.color.BLACK,
                             width=200,
                             align='center'
                             )
        self.box_layout.add(lose_label)

        second_lose_label = UILabel(text=self.lose_text,
                                    font_size=20,
                                    text_color=arcade.color.BLACK,
                                    width=200,
                                    align='center'
                                    )
        self.box_layout.add(second_lose_label)

        continue_button = UITextureButton(text='Продолжить',
                                          width=130,
                                          height=50,
                                          texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                          )
        continue_button.on_click = self.continue_game
        self.buttons_layout.add(continue_button)

        end_button = UITextureButton(text='Выйти',
                                     width=50,
                                     height=50,
                                     texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                     )
        end_button.on_click = self.end_game
        self.buttons_layout.add(end_button)

    def continue_game(self, event):
        self.view.restart()
        self.window.show_view(self.view)

    def end_game(self, event):
        self.message_box = UIMessageBox(message_text='Вы действительно хотите выйти?',
                                        width=400,
                                        height=200,
                                        buttons=('Да', 'Нет'))
        self.message_box.on_action = self.on_message_box
        self.manager.add(self.message_box)

    def on_message_box(self, button_text):
        if button_text.action == 'Да':
            arcade.Window.close(self.window)
        else:
            self.manager.remove(self.message_box)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 5, self.height // 5, self.width - 2 * self.width // 5,
                                          self.height - 2 * self.height // 5, arcade.color.LIGHT_GRAY)
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


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
        if str(event.new_value) != '' and str(event.new_value).isdigit():
            if int(event.new_value) > self.money:
                self.bet_value.text = str(self.money)
            elif int(event.new_value) < 0:
                self.bet_value.text = '0'
            self.bet = int(event.new_value)
        else:
            self.bet_value.text = '0'

    def add_hundred(self, event):
        self.bet += 100
        if self.bet > self.money:
            self.bet = int(self.money)
        self.bet_value.text = str(self.bet)

    def add_quarter(self, event):
        self.bet += 250
        if self.bet > self.money:
            self.bet = int(self.money)
        self.bet_value.text = str(self.bet)

    def add_five_hundred(self, event):
        self.bet += 500
        if self.bet > self.money:
            self.bet = int(self.money)
        self.bet_value.text = str(self.bet)

    def save_bet(self, event):
        if self.bet:
            self.view.bet_done = True
            self.view.first_bet = self.bet
            self.window.show_view(self.view)
            return True

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


class InsuranceView(arcade.View):
    def __init__(self, coins, bet, view):
        super().__init__()
        self.coins = coins
        self.bet = bet
        self.view = view

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        label = UILabel(text='Ставка "Страховка"!',
                        font_size=35,
                        text_color=arcade.color.BLACK,
                        width=200,
                        align='center'
                        )
        self.box_layout.add(label)

        second_label = UILabel(text=f'Ваша ставка: {self.bet}. Ставка "Страховка": {self.bet // 2}',
                               font_size=25,
                               text_color=arcade.color.BLACK,
                               width=200,
                               align='center'
                               )
        self.box_layout.add(second_label)

        if self.coins < self.bet // 2:
            second_label.text = 'Ваш баланс не позволяет участвовать в данной ставке'

            continue_btn = UITextureButton(text='Продолжить',
                                           width=100,
                                           height=50,
                                           texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                           )
            continue_btn.on_click = self.continue_game
            self.box_layout.add(continue_btn)
        else:
            self.buttons_layout = UIBoxLayout(vertical=False, space_between=50)

            take_member = UILabel(text='Участвовать?',
                                  font_size=20,
                                  text_color=arcade.color.BLACK,
                                  width=150,
                                  align='center'
                                  )
            self.box_layout.add(take_member)

            deny_btn = UITextureButton(text='Нет',
                                       width=100,
                                       height=50,
                                       texture=arcade.make_soft_square_texture(100, arcade.color.RED, 255, 255)
                                       )
            deny_btn.on_click = self.continue_game

            accept_btn = UITextureButton(text='Да',
                                         width=100,
                                         height=50,
                                         texture=arcade.make_soft_square_texture(100, arcade.color.GREEN, 255, 255))
            accept_btn.on_click = self.do_bet

            self.buttons_layout.add(deny_btn)
            self.buttons_layout.add(accept_btn)
            self.box_layout.add(self.buttons_layout)

    def continue_game(self, event):
        self.view.insurance_bet = 0
        self.view.insurance_bet_done = True
        self.window.show_view(self.view)

    def do_bet(self, event):
        self.view.insurance_bet_done = True
        self.view.insurance_bet = self.bet // 2
        self.view.coins -= self.view.insurance_bet
        self.view.label.text = str(self.view.coins)
        self.window.show_view(self.view)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 5, self.height // 5, self.width - 2 * self.width // 5,
                                          self.height - 2 * self.height // 5, arcade.color.LIGHT_GRAY)
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


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
        menu_btn = UITextureButton(text='Вернуться',
                                   width=150,
                                   height=50,
                                   texture=arcade.make_soft_square_texture(100, arcade.color.LIGHT_BLUE, 255, 255))
        menu_btn.on_click = self.return_back

        volume_label = UILabel(text='Громкость',
                               width=160,
                               height=50,
                               font_size=20,
                               align='center')

        volume_slider = UISlider(min_value=0, max_value=100, step=1, value=25)
        volume_slider.on_change = change_volume

        self.box_layout.add(volume_label)
        self.box_layout.add(volume_slider)
        self.box_layout.add(menu_btn)

    def on_draw(self):
        self.clear()
        self.view.on_draw()
        arcade.draw_lbwh_rectangle_filled(self.width // 4, self.height // 4, self.width // 2, self.height // 2,
                                          arcade.color.GRAY)
        self.manager.draw()

    def return_back(self, event):
        self.window.show_view(self.view)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()


class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GREEN

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=50)
        self.buttons_layout = UIBoxLayout(vertical=False, space_between=30)

        self.setup_widgets()

        self.box_layout.add(self.buttons_layout)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        over_label = UILabel(text='Вы потеряли весь баланс',
                             width=200,
                             height=60,
                             font_size=35,
                             align='center')
        self.box_layout.add(over_label)

        restart_btn = UITextureButton(text='Начать заново',
                                      width=180,
                                      height=80,
                                      texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255)
                                      )
        restart_btn.on_click = self.restart
        self.buttons_layout.add(restart_btn)

        menu_btn = UITextureButton(text='Вернуться в меню',
                                   width=200,
                                   height=80,
                                   texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        menu_btn.on_click = self.menu
        self.buttons_layout.add(menu_btn)

        exit_btn = UITextureButton(text='Выйти',
                                   width=200,
                                   height=80,
                                   texture=arcade.make_soft_square_texture(100, arcade.color.BLACK, 255, 255))
        exit_btn.on_click = self.exit
        self.buttons_layout.add(exit_btn)

    def restart(self, event):
        view = GameView()
        self.window.show_view(view)

    def menu(self, event):
        view = MenuView()
        self.window.show_view(view)

    def exit(self, event):
        self.message_box = UIMessageBox(message_text='Вы действительно хотите выйти?',
                                        width=400,
                                        height=200,
                                        buttons=('Да', 'Нет'))
        self.message_box.on_action = self.on_message_box
        self.manager.add(self.message_box)

    def on_message_box(self, button_text):
        if button_text.action == 'Да':
            arcade.Window.close(self.window)
        else:
            self.manager.remove(self.message_box)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
