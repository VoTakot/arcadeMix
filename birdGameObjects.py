import arcade


class Bird(arcade.Sprite):
    def __init__(self, win=False, lose=False, speed=125):
        super().__init__()

        self.win = win
        self.lose = lose
        self.move = False
        self.textures = ['images/bird.png', 'images/bird_fly.png']
        self.speed = speed
        self.animation_timer = 0
        self.current_texture = 0
        self.texture_change_delay = 0.1

        if lose:
            self.texture = arcade.load_texture('images/bird_dead.png')
            self.scale = 2
        elif win:
            self.texture = arcade.load_texture('images/king_bird.png')
            self.scale = 2
        else:
            self.texture = arcade.load_texture('images/bird.png')
            self.scale = 0.75

    def update(self, delta_time):
        if self.move:
            self.center_x += self.speed * delta_time
        if not self.win and not self.lose:
            self.animation_timer += delta_time
            if self.animation_timer >= self.texture_change_delay:
                self.animation_timer = 0
                self.current_texture += 1
                if self.current_texture == 2:
                    self.current_texture = 0
                self.texture = arcade.load_texture(self.textures[self.current_texture])

class Colon(arcade.Sprite):
    def __init__(self, colon_type, speed=125):
        super().__init__()
        self.speed = speed
        if colon_type == 'up':
            self.texture = arcade.load_texture('images/colomn_up.png')
        else:
            self.texture = arcade.load_texture('images/colomn_bottom.png')

    def update(self, delta_time):
        self.center_x -= self.speed * delta_time



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
