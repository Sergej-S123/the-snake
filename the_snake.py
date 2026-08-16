import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = GRID_WIDTH // 2, GRID_HEIGHT // 2
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

MOVEMENT_KEYS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}

# Цвета фона, яблока и змейки:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SNAKE_SPEED = 10


TOP_LEFT_CORNER = (0, 0)
# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

pg.init()


class GameObject:
    """Класс для наследования объектов игры."""

    def __init__(
        self,
        body_color=BOARD_BACKGROUND_COLOR,
        position=SCREEN_CENTER
    ):
        self.body_color = body_color

    def draw(self):
        """Отрисовка фигур."""
        raise NotImplementedError("Не реализована функция draw()!")

    def draw_cell(self, position, color=None):
        """Отрисовка ячеек."""
        x, y = position
        color = color or self.body_color
        pg.draw.rect(
            screen,
            color,
            (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_cells):
        super().__init__(
            APPLE_COLOR,
            position=self.randomize_position(occupied_cells)
        )

    def draw(self):
        """Отрисовка ячейки на игровом поле."""
        self.draw_cell(self.position)

    def randomize_position(self, occupied_cells):
        """Генерация яблока."""
        self.position = (random.randint(0, GRID_WIDTH - 1),
                         random.randint(0, GRID_HEIGHT - 1))
        while self.position in occupied_cells:
            self.position = (random.randint(0, GRID_WIDTH - 1),
                             random.randint(0, GRID_HEIGHT - 1))


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, direction=RIGHT):
        super().__init__(SNAKE_COLOR)
        self.positions = [(SCREEN_CENTER)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1

    def move(self):
        """Инициализация движения."""
        head = self.get_head_position()
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH,
                    (head[1] + self.direction[1]) % GRID_HEIGHT)

        # Перемещение головы змейки
        self.positions.insert(0, new_head)

        # Удаление последнего элемента змейки при движении
        if self.snake_cells_amount() > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка на игровом поле."""
        for cell in self.positions:
            self.draw_cell(cell)

    def update_direction(self, new_direction):
        """Смена направления движения змейки."""
        if (-new_direction[0], -new_direction[1]) != self.direction:
            self.direction = new_direction

    def reset(self):
        """Сброс позиции и длинны змейки."""
        self.positions = [(SCREEN_CENTER)]
        self.direction = RIGHT
        self.length = 1

    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]

    def snake_cells_amount(self):
        """Получить длинну змейки."""
        return len(self.positions)


def draw_game_area(snake, apple):
    """Отрисовка игрового поля."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()
    apple.draw()


def reset_game(snake, apple):
    """Сброс параметров игры."""
    snake.reset()
    apple.randomize_position(snake.positions)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if (game_object.direction, event.key) in MOVEMENT_KEYS:
                game_object.next_direction = MOVEMENT_KEYS[
                    (game_object.direction, event.key)
                ]


def main():
    """Основная функция."""
    pg.init()
    pg.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SNAKE_SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()

        # Рестарт игры при столкновении змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            reset_game(snake, apple)

        # Увеличение длинны змейки при съедании яблока
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        draw_game_area(snake, apple)
        pg.display.update()


if __name__ == '__main__':
    main()
