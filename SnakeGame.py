import arcade
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Змейка на Arcade"

GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

MOVEMENT_SPEED = 7.5
BACKGROUND_COLOR = arcade.color.DARK_GREEN
GRID_COLOR = arcade.color.GREEN_YELLOW
SNAKE_COLOR = arcade.color.YELLOW
FOOD_COLOR = arcade.color.RED
TEXT_COLOR = arcade.color.WHITE
SCORE_BOX_COLOR = arcade.color.BLACK

class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.snake = []
        self.snake_direction = (1, 0)
        self.snake_speed = MOVEMENT_SPEED
        self.time_since_move = 0

        self.food = None
        self.obstacles = []

        self.score = 0
        self.game_over = False
        self.paused = False

        self.score_box_width = 150
        self.score_box_height = 50
        self.score_box_x = 10
        self.score_box_y = SCREEN_HEIGHT - self.score_box_height - 10

        self.score_text = arcade.Text(
            f"Счет: {self.score}",
            self.score_box_x + 10, self.score_box_y + 10,
            TEXT_COLOR, 20, bold=True
        )

        self.game_over_text = arcade.Text(
            "ИГРА ОКОНЧЕНА!",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30,
            arcade.color.RED, 40,
            align="center", anchor_x="center", anchor_y="center"
        )

        self.final_score_text = arcade.Text(
            f"Финальный счет: {self.score}",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
            TEXT_COLOR, 30,
            align="center", anchor_x="center", anchor_y="center"
        )

        self.restart_text = arcade.Text(
            "Нажмите ПРОБЕЛ для новой игры",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80,
            TEXT_COLOR, 20,
            align="center", anchor_x="center", anchor_y="center"
        )

        self.reset_game()

        arcade.set_background_color(BACKGROUND_COLOR)

        arcade.schedule(self.update, 1.0 / MOVEMENT_SPEED)

    def reset_game(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]

        self.snake_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.snake_speed = MOVEMENT_SPEED

        self.create_food()
        self.create_obstacles(count=15)

    def create_food(self):
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1)
            food_y = random.randint(0, GRID_HEIGHT - 1)
            if (food_x, food_y) not in self.snake and (food_x, food_y) not in self.obstacles:
                self.food = (food_x, food_y)
                break

    def create_obstacles(self, count=5):
        self.obstacles = []
        for _ in range(count):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if (x, y) not in self.snake and (x, y) != self.food and (x, y) not in self.obstacles:
                    self.obstacles.append((x, y))
                    break

    def on_draw(self):
        self.clear()
        self.draw_grid()

        for i, segment in enumerate(self.snake):
            color = arcade.color.GOLD if i == 0 else SNAKE_COLOR
            x = segment[0] * GRID_SIZE + 1
            y = segment[1] * GRID_SIZE + 1
            size = GRID_SIZE - 2
            arcade.draw_lbwh_rectangle_filled(x, y, size, size, color)

        if self.food:
            x = self.food[0] * GRID_SIZE + GRID_SIZE // 2
            y = self.food[1] * GRID_SIZE + GRID_SIZE // 2
            arcade.draw_circle_filled(x, y, GRID_SIZE // 2 - 2, FOOD_COLOR)

        for obstacle in self.obstacles:
            x = obstacle[0] * GRID_SIZE + GRID_SIZE // 2
            y = obstacle[1] * GRID_SIZE + GRID_SIZE // 2
            size = GRID_SIZE - 4
            left = x - size / 2
            right = x + size / 2
            bottom = y - size / 2
            top = y + size / 2
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.GRAY)

        arcade.draw_lrbt_rectangle_filled(
            self.score_box_x,
            self.score_box_x + self.score_box_width,
            self.score_box_y,
            self.score_box_y + self.score_box_height,
            SCORE_BOX_COLOR
        )

        self.score_text.x = self.score_box_x + 10
        self.score_text.y = self.score_box_y + 10
        self.score_text.draw()

        if self.game_over:
            self.final_score_text.text = f"Финальный счет: {self.score}"
            self.game_over_text.draw()
            self.final_score_text.draw()
            self.restart_text.draw()

        if self.paused:
            # Черный фон и сообщение
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, arcade.color.BLACK)
            pause_text = arcade.Text(
                "ПАУЗА (нажмите ESC для продолжения)",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                arcade.color.WHITE, 40,
                anchor_x="center", anchor_y="center"
            )
            pause_text.draw()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.GREEN_YELLOW, 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.GREEN_YELLOW, 1)

    def update(self, delta_time):
        if self.game_over or self.paused:
            return
        self.move_snake()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.snake_direction
        new_head = (head_x + dx, head_y + dy)

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        if new_head in self.obstacles:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.score_text.text = f"Счет: {self.score}"
            self.create_food()

            if self.score % 50 == 0:
                self.snake_speed += 1
                arcade.unschedule(self.update)
                arcade.schedule(self.update, 1.0 / self.snake_speed)
        else:
            self.snake.pop()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.reset_game()
            return
        if key == arcade.key.ESCAPE:
            if not self.game_over:
                self.paused = not self.paused
            return
        if self.game_over:
            return

        if key == arcade.key.UP and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif key == arcade.key.DOWN and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif key == arcade.key.LEFT and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif key == arcade.key.RIGHT and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)

    def on_close(self):
        arcade.unschedule(self.update)
        super().on_close()

def main():
    game = SnakeGame()
    arcade.run()

if __name__ == "__main__":
    main()