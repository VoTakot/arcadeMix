from GameScenes import MenuView
import arcade

if __name__ == '__main__':
    window = arcade.Window(1000, 600, "Flappy Bird")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
