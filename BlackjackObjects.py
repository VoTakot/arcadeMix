import arcade
import sqlite3

connection = sqlite3.connect('cards.db')

cursor = connection.cursor()


class Card(arcade.Sprite):
    def __init__(self, card):
        super().__init__()

        card_data = cursor.execute("""
        select texture, points
        from CARDS
        where id = ?
        """, (card,)).fetchall()

        self.texture = arcade.load_texture(str(card_data[0][0]))
        if int(card_data[0][1]) != 11:
            self.points = int(card_data[0][1])
        else:
            self.points = (1, 11)


class Hand(arcade.Sprite):
    def __init__(self, card_owner, card_number):
        super().__init__()
        self.texture = arcade.load_texture('game_images/hand.png')
        self.go_to_x = 0
        self.go_to_y = 0

        self.card_owner = card_owner
        self.card_number = card_number

        self.going_back = False

        self.total_cord_x = False
        self.total_cord_y = False
        self.place_card = False

    def update(self, delta_time):
        if self.card_owner == 'player':
            self.go_to_y = 475
            self.go_to_x = 210 + self.card_number * 120
        elif self.card_owner == 'dealer':
            self.go_to_y = 717
            self.go_to_x = 210 + self.card_number * 120
        if self.center_x >= self.go_to_x:
            self.center_x = self.go_to_x
            self.total_cord_x = True
        if self.center_y <= self.go_to_y:
            self.center_y = self.go_to_y
            self.total_cord_y = True
        if self.total_cord_x and self.total_cord_y:
            if self.center_y - 1 <= self.go_to_y:
                self.place_card = True
            self.going_back = True
            self.center_y += 450 * delta_time
        if self.center_x < self.go_to_x and not (self.total_cord_x and self.total_cord_y):
            self.center_x += 450 * delta_time
        if self.center_y > self.go_to_y and not (self.total_cord_x and self.total_cord_y):
            self.center_y -= 450 * delta_time
        if self.center_y - self.height // 2 >= 750 and self.total_cord_y and self.total_cord_y:
            self.center_x += 120
            self.center_y = 1200
            self.total_cord_y = False
            self.total_cord_x = False
            self.going_back = False
