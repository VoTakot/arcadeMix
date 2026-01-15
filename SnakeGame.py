import arcade

TILE_SCALING = 0.5

class GridGame(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, "Пример клеточного поля со спрайтами")

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        map_name = "snakemap.tmx"
        tile_map = arcade.load_tilemap(map_name)

        self.wall_list = tile_map.sprite_lists["walls"]
        self.collision_list = tile_map.sprite_lists["collision"]
        #пока так
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            0.5)
        self.player_sprite.center_x = 128  # Примерные координаты
        self.player_sprite.center_y = 256  # Примерные координаты
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()


def main():
    game = GridGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()