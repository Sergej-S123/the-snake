import random
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SNAKE_SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

pygame.init()


class GameObject:
    """Класс объектов игры."""

    def __init__(self):
        body_color = BOARD_BACKGROUND_COLOR
        self.body_color = body_color
        self.position = SCREEN_CENTER_X, SCREEN_CENTER_Y

    def draw(self):
        """Отрисовка фигур."""
        pass

    def draw_cell(self, position, color=None):
        """Отрисовка ячеек."""
        x, y = position
        color = color or self.body_color
        pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE,
                                         GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__()
        self.position = None
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка ячейки на игровом поле."""
        self.draw_cell(self.position)


    def randomize_position(self, snake_body):
        """Генерация яблока."""
        self.position = (random.randint(0, GRID_WIDTH - 1),
                         random.randint(0, GRID_HEIGHT - 1))
        while self.position in snake_body:
            self.position = (random.randint(0, GRID_WIDTH - 1),
                             random.randint(0, GRID_HEIGHT - 1))


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1

    def move(self):
        """Инициализация движения."""
        head = self.positions[0]
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH,
                    (head[1] + self.direction[1]) % GRID_HEIGHT)

        # Рестарт игры при столкновении змейки с собой
        if new_head in self.positions:
            reset_game(snake, apple)
            return False

        # Удаление последнего элемента змейки при движении
        self.positions.insert(0, new_head)
        if self.get_length() > self.length:
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
        """Сброс позиции змейки."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT

    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]

    def get_length(self):
        """Получить длинну змейки."""
        return len(self.positions)


def draw_game_area(snake, apple):
    """Отрисовка игрового поля."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    for cell in snake.positions:
        snake.draw_cell(cell)
    apple.draw()


def reset_game(snake, apple):
    """Сброс параметров игры."""
    snake.reset()
    apple.randomize_position(snake.positions)
    snake.length = 1


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


snake = Snake()
apple = Apple()


def main():
    """Основная функция."""
    pygame.init()
    pygame.display.set_caption('Змейка')
    reset_game(snake, apple)

    while True:
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1
        draw_game_area(snake, apple)
        pygame.display.update()
        clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    main()
