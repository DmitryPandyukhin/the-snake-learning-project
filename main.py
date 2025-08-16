'''Главный модуль программы.
Игра "Змейка".
'''
import tkinter as tk
import random

# Настройки игры
WIDTH_PLAYING_FIELD = 400
HEIGHT_PLAYING_FIELD = 400
CELL_SIZE = 10
DELAY = 100 # Скорость игры (задержка между движениями змейки в мс)
DIRECTIONS = [ "Up", "Left", "Down", "Right"]

# Создание главного окна
main_window = tk.Tk()
main_window.title("Змейка | Счет: 0")
main_window.resizable(False, False)

# Холст для рисования
canvas = tk.Canvas(
    main_window,
    width=WIDTH_PLAYING_FIELD,
    height=HEIGHT_PLAYING_FIELD,
    bg="black",
    highlightthickness=0,
)
canvas.pack()

# Начальное состояние игры
snake = [ (100, 100), (90, 100), (80, 100)]

# pylint: disable=invalid-name / C0103
direction = "Right"
score = 0
game_over = False

def create_food():
    """Создание еды."""
    while True:
        x = random.randint(0, (WIDTH_PLAYING_FIELD - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT_PLAYING_FIELD - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = create_food()

def draw_food():
    """Отрисовка еды."""
    canvas.create_rectangle(
        food[0], food[1],
        food[0] + CELL_SIZE, food[1] + CELL_SIZE,
        fill="red"
    )

def draw_snake():
    """Отрисовка змейки"""
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE, segment[1] + CELL_SIZE,
            fill="green",
            outline="darkgreen"
        )

def check_well_collision():
    """Проверка выхода за пределы игрового поля."""
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDTH_PLAYING_FIELD or
        head_y < 0 or head_y >= HEIGHT_PLAYING_FIELD
    )

def end_game():
    """Завершение игры"""
    # pylint: disable=global-statement / W0603
    global game_over
    game_over = True
    canvas.create_text(
        WIDTH_PLAYING_FIELD // 2,
        HEIGHT_PLAYING_FIELD // 2,
        text = "Игра окончена! Счет: " + str(score),
        fill="white",
        font=("Arial", 24)
    )

def restart_game():
    '''Перезапускаем игру.'''
    # pylint: disable=global-statement / W0603
    global snake, direction, food, score, game_over

    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "Right"

    food = create_food()

    score = 0
    game_over = False

    # Очистим холст и обновим
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_window_title()

    # Перезапускаем игровой цикл
    main_window.after(DELAY, game_loop)


def on_key_press(event):
    """Обработка нажатия клавиш."""
    # pylint: disable=global-statement / W0603
    global direction
    key = event.keysym
    if key in DIRECTIONS:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
    elif key == "space" and game_over:
        restart_game()

main_window.bind("<KeyPress>", on_key_press) # Привязка обработчик к окну.

def check_food_collision():
    """Проверяем, съедена ли еда."""
    # pylint: disable=global-statement / W0603
    global food, score
    if snake[0] == food:
        score += 1
        food = create_food()
        return True
    return False

def move_snake():
    """Двигаем змейку."""
    head_x, head_y = snake[0]
    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)
    else:
        new_head = (head_x, head_y)

    snake.insert(0, new_head)

    if not check_food_collision():
        snake.pop()

def update_window_title():
    """Обновняем счет"""
    main_window.title(f"Змейка | Счет: {score}")

def check_self_collision():
    """Проверка того, что змейка врезается самв в себя."""    
    return snake[0] in snake[1:]


def game_loop():
    """Игровой цикл."""
    if game_over:
        return

    move_snake()

    if check_well_collision() or check_self_collision():
        end_game()
        return

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_window_title()
    main_window.after(DELAY, game_loop)

draw_food()
draw_snake()
main_window.after(DELAY, game_loop)

# Запуск главного цикла
main_window.mainloop()
