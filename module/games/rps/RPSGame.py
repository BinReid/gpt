import pygame
import random

pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Камень, ножницы, бумага")

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Загрузка изображений
rock_img = pygame.image.load('data/rock.png')
paper_img = pygame.image.load('data/paper.png')
scissors_img = pygame.image.load('data/scissor.jpg')

# Масштабирование изображений
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))

# Фоновое изображение
background = pygame.image.load('data/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def main():
    running = True
    player_choice = None
    computer_choice = None
    result = ""

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    player_choice = "rock"
                elif event.key == pygame.K_x:
                    player_choice = "paper"
                elif event.key == pygame.K_c:
                    player_choice = "scissors"

                if player_choice:
                    computer_choice = random.choice(["rock", "paper", "scissors"])
                    result = determine_winner(player_choice, computer_choice)

        # Отображение выборов
        if player_choice:
            screen.blit(
                rock_img if player_choice == "rock" else paper_img if player_choice == "paper" else scissors_img,
                (150, 300))

        if computer_choice:
            screen.blit(
                rock_img if computer_choice == "rock" else paper_img if computer_choice == "paper" else scissors_img,
                (500, 300))

        # Отображение результата
        result_color = GREEN if "Вы выиграли" in result else RED if "Вы проиграли" in result else WHITE
        result_text = font.render(result, True, result_color)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))

        # Инструкции
        instruction_text = small_font.render("Нажмите Z для камня, X для бумаги, C для ножниц", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 500))

        pygame.display.flip()

    pygame.quit()


def determine_winner(player, computer):
    if player == computer:
        return "Ничья!"
    elif (player == "rock" and computer == "scissors") or \
            (player == "scissors" and computer == "paper") or \
            (player == "paper" and computer == "rock"):
        return "Вы выиграли!"
    else:
        return "Вы проиграли!"


if __name__ == "__main__":
    main()
