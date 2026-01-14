import arcade


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('images/bird.png')

    def update(self, delta_time):
        pass


class Colon(arcade.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'up':
            self.texture = arcade.load_texture('images/colomn_up.png')
        else:
            self.texture = arcade.load_texture('images/colomn_bottom.png')

    def update(self, delta_time):
        pass


class Finish(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('images/finish.png')

    def update(self, delta_time):
        pass

class Earth(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('images/earth.png')