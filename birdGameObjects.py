import arcade


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('images/bird.png')
        self.scale = 0.75

    def update(self, delta_time):
        self.center_x += 75 * delta_time


class Colon(arcade.Sprite):
    def __init__(self, colon_type):
        super().__init__()
        self.colon_deleted = False
        if colon_type == 'up':
            self.texture = arcade.load_texture('images/colomn_up.png')
        else:
            self.texture = arcade.load_texture('images/colomn_bottom.png')

    def update(self, delta_time):
        self.center_x -= 125 * delta_time



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
