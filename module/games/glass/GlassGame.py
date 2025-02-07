import pygame
import random
import sys
import time
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра в Стеклянные Мосты")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
GLASS_COLOR = (173, 216, 230)  # Светло-голубой для стекол

# Шрифты
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Загрузка фона
try:
    background = pygame.image.load("data/backgroundglass.png")  # Замените на ваш файл фона
except FileNotFoundError:
    print("Файл фона не найден. Убедитесь, что 'background.png' находится в той же папке.")
    sys.exit()

# Масштабирование фона под размеры окна
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# Класс для стекол
class Glass:
    def __init__(self, x, y, width, height, is_safe):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_safe = is_safe
        self.revealed = False
        self.selected = False

    def draw(self, screen):
        if self.revealed:
            color = GREEN if self.is_safe else RED
        else:
            color = GLASS_COLOR if not self.selected else YELLOW  # Подсветка выбранного стекла
        pygame.draw.rect(screen, color, self.rect, border_radius=10)  # Закругленные углы
        if self.selected:
            pygame.draw.rect(screen, YELLOW, self.rect, width=3, border_radius=10)  # Обводка выбранного стекла


# Функция для отрисовки крестика
def draw_cross(screen, rect, color):
    # Рисуем две диагональные линии
    pygame.draw.line(screen, color, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), 5)
    pygame.draw.line(screen, color, (rect.x + rect.width, rect.y), (rect.x, rect.y + rect.height), 5)


# Функция для анимации покачивания камеры
def shake_screen(offset):
    screen.blit(background, (offset, 0))  # Сдвигаем фон по горизонтали


# Основная функция игры
def main():
    # Настройки уровня сложности (по умолчанию легкий)
    lives = 3  # Количество жизней в легком режиме
    num_pairs = 5  # Количество пар стекол
    current_pair = 0  # Текущая пара стекол

    # Основной игровой цикл
    running = True
    game_over = False
    selected_glass = None
    result_text = ""
    result_color = WHITE
    glasses = []
    show_result = False  # Показывать ли результат выбора
    result_start_time = 0  # Время появления результата
    last_selected_glass = None  # Сохраняем последнее выбранное стекло для отображения текста
    shake_offset = 0  # Смещение для анимации покачивания камеры
    shake_duration = 0  # Длительность анимации покачивания

    while running:
        screen.fill(BLACK)  # Очистка экрана

        # Анимация покачивания камеры
        if shake_duration > 0:
            shake_offset = 5 * math.sin(time.time() * 20)  # Синусоидальное смещение
            shake_duration -= 1
        else:
            shake_offset = 0

        # Отрисовка фона с учетом смещения
        screen.blit(background, (shake_offset, 0))

        if game_over:
            # Экран проигрыша
            draw_text("Вы проиграли!", WIDTH // 2 - 150, HEIGHT // 2 - 50, RED, large_font)
            draw_text("Нажмите ESC для выхода", WIDTH // 2 - 200, HEIGHT // 2 + 50, WHITE)
        else:
            # Создание стекол только при начале новой пары
            if current_pair < num_pairs and not glasses:
                # Позиции стекол
                glass1 = Glass(200, 200, 250, 200, random.choice([True, False]))  # Левое стекло
                glass2 = Glass(550, 200, 250, 200, not glass1.is_safe)  # Правое стекло
                glasses = [glass1, glass2]

            # Отрисовка стекол
            for glass in glasses:
                glass.draw(screen)

            # Отрисовка результата выбора под стеклом
            if show_result and time.time() - result_start_time < 1:  # Показывать результат 1 секунду
                if last_selected_glass:
                    text_x = last_selected_glass.rect.centerx - 50  # Центрируем текст под стеклом
                    text_y = last_selected_glass.rect.bottom + 10  # Позиция под стеклом
                    draw_text(result_text, text_x, text_y, result_color, font)
            else:
                show_result = False  # Скрыть результат после 1 секунды

            # Отрисовка текста
            draw_text(f"Жизни: {lives}", 10, 10)
            draw_text(f"Пара: {current_pair + 1}/{num_pairs}", 10, 50)

            # Подсказка для игрока
            if selected_glass is None:
                draw_text("Выберите стекло", WIDTH // 2 - 100, 100, WHITE, font)
            else:
                draw_text("Нажмите ПРОБЕЛ чтобы прыгнуть", WIDTH // 2 - 200, 100, WHITE, font)

            # Если все пары пройдены
            if current_pair >= num_pairs:
                draw_text("Вы прошли все пары!", WIDTH // 2 - 150, HEIGHT // 2, GREEN, large_font)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not game_over:
                    if current_pair < num_pairs:
                        # Выбор стекла
                        if selected_glass is None:
                            for glass in glasses:
                                if glass.rect.collidepoint(pos):
                                    selected_glass = glass
                                    glass.selected = True
                                    result_text = ""
                                    result_color = WHITE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and selected_glass is not None:
                    if selected_glass.is_safe:
                        result_text = "Правильно!"
                        result_color = GREEN
                        current_pair += 1
                    else:
                        lives -= 1
                        if lives == 0:
                            game_over = True
                        else:
                            result_text = "Ошибка!"
                            result_color = RED
                    show_result = True  # Показать результат
                    result_start_time = time.time()  # Засечь время появления результата
                    last_selected_glass = selected_glass  # Сохраняем выбранное стекло для отображения текста
                    selected_glass.revealed = True
                    selected_glass.selected = False
                    selected_glass = None
                    glasses = []  # Сбрасываем стекла для следующей пары
                    shake_duration = 30  # Запуск анимации покачивания камеры
                if event.key == pygame.K_ESCAPE and game_over:
                    running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Функция для отображения текста
def draw_text(text, x, y, color=WHITE, font_type=font):
    text_surface = font_type.render(text, True, color)
    screen.blit(text_surface, (x, y))


if __name__ == "__main__":
    main()