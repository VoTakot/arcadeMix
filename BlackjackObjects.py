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
        print(card_data[0])

        self.texture = arcade.load_texture(str(card_data[0][0]))
        if int(card_data[0][1]) != 11:
            self.points = int(card_data[0][1])
        else:
            self.points = (1, 11)