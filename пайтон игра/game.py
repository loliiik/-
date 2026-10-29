# Название: Наш Спецназ
# Жанр: Шутер
# Идея в одном предложении: Зачистка
# Размер окна: 1920 x 1080
# Цветовая гамма: черно-белая

# Импорт
import pygame

# Константы
WIDTH = 1920
HEIGHT = 1080
FPS = 60
BG_COLOR = (0, 0, 0)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Наш Спецназ")
clock = pygame.time.Clock()

# Главный цикл
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    pygame.display.update()

pygame.quit()