import arcade
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Змейка на Arcade"

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

MOVEMENT_SPEED = 10  # Клеток в секунду
BACKGROUND_COLOR = arcade.color.DARK_GREEN
GRID_COLOR = arcade.color.GREEN_YELLOW
SNAKE_COLOR = arcade.color.YELLOW
FOOD_COLOR = arcade.color.RED
TEXT_COLOR = arcade.color.WHITE


class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Инициализация змейки
        self.snake = []
        self.snake_direction = (1, 0)  # Направление движения (dx, dy)
        self.snake_speed = MOVEMENT_SPEED
        self.time_since_move = 0

        # Еда
        self.food = None

        # Состояние игры
        self.score = 0
        self.game_over = False

        # Текстовые объекты для оптимизации
        self.score_text = arcade.Text(
            f"Счет: {self.score}",
            10, SCREEN_HEIGHT - 30,
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

        # Инициализация
        self.reset_game()

        arcade.set_background_color(BACKGROUND_COLOR)

        # Включаем обновление каждые 0.1 секунды
        arcade.schedule(self.update, 1.0 / MOVEMENT_SPEED)

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        # Начальная позиция змейки (3 сегмента в центре)
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
        self.snake_speed = MOVEMENT_SPEED

        # Обновляем текст счета
        self.score_text.text = f"Счет: {self.score}"

        # Создаем первую еду
        self.create_food()

    def create_food(self):
        """Создание еды в случайном месте, не занятом змейкой"""
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1)
            food_y = random.randint(0, GRID_HEIGHT - 1)

            # Проверяем, чтобы еда не появилась на змейке
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    def on_draw(self):
        """Отрисовка игры"""
        # Очищаем экран и начинаем отрисовку
        self.clear()

        # Отрисовка сетки (опционально)
        self.draw_grid()

        # Отрисовка змейки
        for i, segment in enumerate(self.snake):
            # Голова змейки немного темнее
            if i == 0:
                color = arcade.color.GOLD
            else:
                color = SNAKE_COLOR

            # Вычисляем координаты левого нижнего угла прямоугольника
            x = segment[0] * GRID_SIZE + 1  # +1 для отступа от сетки
            y = segment[1] * GRID_SIZE + 1  # +1 для отступа от сетки
            size = GRID_SIZE - 2  # -2 чтобы оставался отступ от сетки

            arcade.draw_lbwh_rectangle_filled(x, y, size, size, color)

        # Отрисовка еды
        if self.food:
            x = self.food[0] * GRID_SIZE + GRID_SIZE // 2
            y = self.food[1] * GRID_SIZE + GRID_SIZE // 2
            arcade.draw_circle_filled(x, y, GRID_SIZE // 2 - 2, FOOD_COLOR)

        # Отрисовка счета (используем объект Text)
        self.score_text.draw()

        # Сообщение о конце игры
        if self.game_over:
            # Обновляем текст финального счета
            self.final_score_text.text = f"Финальный счет: {self.score}"

            self.game_over_text.draw()
            self.final_score_text.draw()
            self.restart_text.draw()

    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, GRID_COLOR, 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, GRID_COLOR, 1)

    def update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_over:
            return

        # Двигаем змейку
        self.move_snake()

    def move_snake(self):
        """Перемещение змейки"""
        # Получаем текущую позицию головы
        head_x, head_y = self.snake[0]

        # Вычисляем новую позицию головы
        dx, dy = self.snake_direction
        new_head = (head_x + dx, head_y + dy)

        # Проверяем столкновение с границами
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        # Проверяем столкновение с собой
        if new_head in self.snake:
            self.game_over = True
            return

        # Добавляем новую голову
        self.snake.insert(0, new_head)

        # Проверяем, съела ли змейка еду
        if new_head == self.food:
            self.score += 10
            self.score_text.text = f"Счет: {self.score}"  # Обновляем текст счета
            self.create_food()

            # Увеличиваем скорость каждые 50 очков
            if self.score % 50 == 0:
                self.snake_speed += 1
                # Обновляем интервал обновления
                arcade.unschedule(self.update)
                arcade.schedule(self.update, 1.0 / self.snake_speed)
        else:
            # Удаляем хвост, если не съели еду
            self.snake.pop()

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if self.game_over and key == arcade.key.SPACE:
            self.reset_game()
            return

        if self.game_over:
            return

        # Управление змейкой
        if key == arcade.key.UP and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif key == arcade.key.DOWN and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif key == arcade.key.LEFT and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif key == arcade.key.RIGHT and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)

        # Пауза
        elif key == arcade.key.P:
            self.game_over = not self.game_over

    def on_close(self):
        """При закрытии окна"""
        arcade.unschedule(self.update)
        super().on_close()


def main():
    """Основная функция"""
    game = SnakeGame()
    arcade.run()


if __name__ == "__main__":
    main()