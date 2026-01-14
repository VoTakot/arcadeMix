import arcade
from birdGameObjects import Bird, Colon, Earth

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Flappy Bird'


class FlappyBird(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE)
        self.width = width
        self.height = height
        self.game_over = False

    def setup(self):
        self.bird_list = arcade.SpriteList()
        self.earth_list = arcade.SpriteList()
        self.colons_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.bird = Bird()
        self.bird.center_x = 100
        self.bird.center_y = SCREEN_HEIGHT // 2
        self.bird_list.append(self.bird)
        for i in range(self.width // 100 + 1):
            earth = Earth()
            earth.center_x = 100 * i
            earth.center_y = 50
            self.earth_list.append(earth)



    def on_update(self, delta_time):
        pass

    def on_draw(self):
        self.clear()
        self.background_color = arcade.color.LIGHT_BLUE
        self.bird_list.draw()
        self.earth_list.draw()
        self.colons_list.draw()


def setup_game(width=1000, height=600):
    game = FlappyBird(width, height)
    game.setup()
    return game


def main():
    game = setup_game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
