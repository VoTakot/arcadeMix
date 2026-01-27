import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Три в ряд"
GRID_SIZE = 8
CELL_SIZE = 60
MARGIN = 50

GEM_COLORS = [
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW,
    arcade.color.PURPLE,
    arcade.color.ORANGE,
    arcade.color.CYAN
]


class GemThreeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.grid = []
        self.selected_gem = None
        self.score = 0
        self.initialize_grid()
        self.error_sound = arcade.load_sound('sounds/fail.mp3')
        self.right_sound = arcade.load_sound('sounds/right.mp3')

    def initialize_grid(self):
        self.grid = []
        for row in range(GRID_SIZE):
            self.grid.append([])
            for col in range(GRID_SIZE):
                color_index = random.randint(0, len(GEM_COLORS) - 1)
                self.grid[row].append(color_index)
        self.remove_matches()

    def on_draw(self):
        self.clear()
        grid_width = GRID_SIZE * CELL_SIZE
        grid_height = GRID_SIZE * CELL_SIZE
        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = (SCREEN_HEIGHT - grid_height) // 2

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = start_x + col * CELL_SIZE + CELL_SIZE // 2
                y = start_y + row * CELL_SIZE + CELL_SIZE // 2
                left = x - CELL_SIZE // 2
                right = x + CELL_SIZE // 2
                top = y + CELL_SIZE // 2
                bottom = y - CELL_SIZE // 2
                arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.LIGHT_GRAY)
                color_index = self.grid[row][col]
                arcade.draw_circle_filled(x, y, CELL_SIZE // 2 - 5, GEM_COLORS[color_index])
                if self.selected_gem == (row, col):
                    arcade.draw_circle_outline(x, y, CELL_SIZE // 2 - 2, arcade.color.WHITE, 3)

        arcade.draw_text(f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)
        arcade.draw_text("Выберите камень и переместите его", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text("с соседним по горизонтали или вертикали", 10, 5, arcade.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            grid_width = GRID_SIZE * CELL_SIZE
            grid_height = GRID_SIZE * CELL_SIZE
            start_x = (SCREEN_WIDTH - grid_width) // 2
            start_y = (SCREEN_HEIGHT - grid_height) // 2

            if start_x <= x < start_x + grid_width and start_y <= y < start_y + grid_height:
                col = int((x - start_x) // CELL_SIZE)
                row = int((y - start_y) // CELL_SIZE)

                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if self.selected_gem is None:
                        self.selected_gem = (row, col)
                    else:
                        self.swap_gems(self.selected_gem, (row, col))
                        self.selected_gem = None

    def swap_gems(self, pos1, pos2):
        row1, col1 = map(int, pos1)
        row2, col2 = map(int, pos2)

        if (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2):
            self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]

            matches = self.find_matches()
            if matches:
                self.process_matches(matches)
                arcade.play_sound(self.right_sound)
            else:
                self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]
                arcade.play_sound(self.error_sound)

    def find_matches(self):
        matches = []

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2):
                if (self.grid[row][col] is not None and
                        self.grid[row][col] == self.grid[row][col + 1] == self.grid[row][col + 2]):
                    match_length = 3
                    while (col + match_length < GRID_SIZE and
                           self.grid[row][col] == self.grid[row][col + match_length]):
                        match_length += 1
                    for i in range(match_length):
                        matches.append((row, col + i))

        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 2):
                if (self.grid[row][col] is not None and
                        self.grid[row][col] == self.grid[row + 1][col] == self.grid[row + 2][col]):
                    match_length = 3
                    while (row + match_length < GRID_SIZE and
                           self.grid[row][col] == self.grid[row + match_length][col]):
                        match_length += 1
                    for i in range(match_length):
                        matches.append((row + i, col))

        return list(set(matches))

    def process_matches(self, matches):
        if not matches:
            return

        self.score += len(matches) * 10

        for row, col in matches:
            self.grid[row][col] = None

        self.drop_gems()
        self.fill_empty_spaces()

        new_matches = self.find_matches()
        if new_matches:
            self.process_matches(new_matches)

    def drop_gems(self):
        for col in range(GRID_SIZE):
            column_gems = []
            for row in range(GRID_SIZE):
                if self.grid[row][col] is not None:
                    column_gems.append(self.grid[row][col])

            for row in range(GRID_SIZE):
                if row < len(column_gems):
                    self.grid[GRID_SIZE - 1 - row][col] = column_gems[len(column_gems) - 1 - row]
                else:
                    self.grid[GRID_SIZE - 1 - row][col] = None

    def fill_empty_spaces(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is None:
                    self.grid[row][col] = random.randint(0, len(GEM_COLORS) - 1)

    def remove_matches(self):
        while True:
            matches = self.find_matches()
            if not matches:
                break
            for row, col in matches:
                self.grid[row][col] = random.randint(0, len(GEM_COLORS) - 1)


def main():
    game = GemThreeGame()
    arcade.run()


if __name__ == '__main__':
    main()