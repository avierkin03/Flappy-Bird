import pygame
from random import randint

# Ініціалізація розміру вікна та створення вікна гри
window_size = (1200, 800)
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Створюємо прямокутник головного гравця
player_rect = pygame.Rect(150, 300, 100, 100)

# Ініціалізація шрифту та змінних гри
score = 0
lose = False
player_speed = 15
pygame.font.init()
main_font = pygame.font.SysFont("Mono", 100)

# Функція для генерації пар труб із заданими парметрами 
def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = pygame.Rect(start_x, 0, pipe_width, height)   # верхня труба
        bottom_pipe = pygame.Rect(start_x, height+gap, pipe_width, window_size[1]-(height+gap)) # нижня труба
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

# створюємо 150 труб
pipes = generate_pipes(150)

# Ігровий цикл
while True:
    for event in pygame.event.get():
        # якщо тип події "Натиснутий хрестик" - зупиняємо програму
        if event.type == pygame.QUIT:
            pygame.quit()

    # Малюємо фон у вікні
    window.fill("sky blue") 

    # малюємо прямокутник гравця
    pygame.draw.rect(window, "yellow", player_rect)

    # Управління гравцем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] == True and not lose:
        player_rect.y -= player_speed            # рух вгору
    if keys[pygame.K_s] == True and not lose:
        player_rect.y += player_speed            # рух вниз

    # Перевірка падіння гравця
    if player_rect.y >= window_size[1] - player_rect.height:
        lose = True

    # Генерація нових труб, якщо їх мало
    if len(pipes) < 8:
        pipes += generate_pipes(150)

    # Обробка труб
    for pipe in pipes[:]:
        if not lose:
            pipe.x -= 10  # рух труби ліворуч
        pygame.draw.rect(window, "green", pipe)
        if pipe.x <= -100:
            pipes.remove(pipe)   # видалення труби
            score += 0.5         # збільшення рахунку
        # зіткнення з трубою = програш   
        if player_rect.colliderect(pipe):
            lose = True

    # оновлення екрану та контроль FPS
    clock.tick(60)
    pygame.display.update()