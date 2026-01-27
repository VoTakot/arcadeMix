import arcade
from BlackjackViews import MenuView

if __name__ == '__main__':
    window = arcade.Window(width=1000, height=800, title='Блекджек')
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
