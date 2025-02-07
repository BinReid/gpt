import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Русская рулетка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

# Шрифты
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)

# Загрузка звуков
shot_sound = pygame.mixer.Sound("data/shot.wav")
empty_sound = pygame.mixer.Sound("data/empty.wav")
click_sound = pygame.mixer.Sound("data/click.wav")

# Загрузка изображений
background = pygame.image.load("data/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Переменные игры
bullets = [0, 0, 0, 0, 0, 1]  # 1 - пуля, 0 - пустой патрон
random.shuffle(bullets)
current_turn = "player"  # Игрок или бот
player_shot_used = False  # Использовал ли игрок выстрел в соперника
bot_shot_used = False  # Использовал ли бот выстрел в соперника
game_over = False
message = ""  # Сообщение о результате выстрела


def draw_text(text, x, y, color=GRAY, font_type=font):
    text_surface = font_type.render(text, True, color)
    screen.blit(text_surface, (x, y))


def reset_game():
    global bullets, current_turn, player_shot_used, bot_shot_used, game_over, message
    bullets = [0, 0, 0, 0, 0, 1]
    random.shuffle(bullets)
    current_turn = "player"
    player_shot_used = False
    bot_shot_used = False
    game_over = False
    message = ""


def bot_turn():
    global current_turn, bot_shot_used, game_over, message
    if not game_over:
        pygame.time.wait(1000)
        click_sound.play()

        if not bot_shot_used and random.random() < 0.2:  # 20% шанс выстрелить в игрока
            bot_shot_used = True
            if bullets.pop(0) == 1:
                message = "Вы умерли!"
                shot_sound.play()
                game_over = True
            else:
                message = "Вы выжили!"
                empty_sound.play()
        else:
            if bullets.pop(0) == 1:
                message = "Противник умер!"
                shot_sound.play()
                game_over = True
            else:
                message = "Противник выжил!"
                empty_sound.play()
        current_turn = "player"


# Основной игровой цикл
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_s:  # Игрок стреляет в себя
                click_sound.play()
                pygame.time.wait(500)
                if bullets.pop(0) == 1:
                    message = "Вы умерли!"
                    shot_sound.play()
                    game_over = True
                else:
                    message = "Вы выжили!"
                    empty_sound.play()
                    current_turn = "bot"
            elif event.key == pygame.K_a and not player_shot_used:  # Игрок стреляет в бота
                player_shot_used = True
                click_sound.play()
                pygame.time.wait(500)
                if bullets.pop(0) == 1:
                    message = "Противник умер!"
                    shot_sound.play()
                    game_over = True
                else:
                    message = "Противник выжил!"
                    empty_sound.play()
                    current_turn = "bot"

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Перезапуск игры
                reset_game()

    # Отображение текста
    draw_text("Русская рулетка", WIDTH // 2 - 150, 20, RED)
    if message:
        draw_text(message, WIDTH // 2 - 100, HEIGHT // 2, GRAY)

    # Отображение правил
    draw_text("S - выстрелить в себя", 20, HEIGHT - 100, GRAY, small_font)
    draw_text("A - выстрелить в бота (1 раз)", 20, HEIGHT - 75, GRAY, small_font)
    draw_text("R - рестарт", 20, HEIGHT - 50, GRAY, small_font)

    pygame.display.flip()

    if not game_over and current_turn == "bot":
        bot_turn()

pygame.quit()
