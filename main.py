import pygame
import random
import time

# Инициализация Pygame
pygame.init()
# Настройки экрана
SCREEN_WIDTH = 1280  # Увеличенный размер окна
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Ограничение FPS
clock = pygame.time.Clock()

pygame.display.set_caption("Звёздный стрелок")
icon = pygame.image.load("image/image_converted.jpeg")
pygame.display.set_icon(icon)

# Загрузка фоновой музыки и её запуск
pygame.mixer.music.load('sounds/506324.wav')  # Загрузка фоновой музыки
pygame.mixer.music.play(-1)  # Зацикливание музыки (играет бесконечно)

# Список фонов
background_images = [
    "backgrounds/1.1.jpeg",  # Космическая туманность
    "backgrounds/2.1.jpeg",  # Футуристический город
    "backgrounds/3.1.jpeg",  # Поверхность инопланетной планеты
    "backgrounds/4.jpeg",  # Кибернетическая сеть
    "backgrounds/5.jpeg",  # Метеоритный дождь
    "backgrounds/6.jpeg",  # Звёздное небо
    "backgrounds/7.1.jpeg"  # Интерьер космического корабля
]

# Выбор случайного фона
selected_background = random.choice(background_images)
background_img = pygame.image.load(selected_background)
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Размеры мишени
target_width = 90
target_height = 90

# Загружаем изображение мишени
target_img = pygame.image.load("image/target4.png")
target_img = pygame.transform.scale(target_img, (target_width, target_height))

# Шрифт для текста
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 40)  # Шрифт для инструкций
large_font = pygame.font.SysFont(None, 70)  # Шрифт для плавающих очков

# Счётчик очков
score = 0

# Таймер для игры
game_time = 30  # Время игры в секундах
start_time = time.time()

# Загрузка звуков
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")
end_game_sound = pygame.mixer.Sound("sounds/game-over.wav")  # Звук окончания игры

# Параметры для анимации вспышки
flash_duration = 1.0
flash_timer = 0
is_flashing = False

# Список для плавающих очков
floating_scores = []

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Класс для плавающих очков
class FloatingScore:
    def __init__(self, x, y, score_value):
        self.x = x
        self.y = y
        self.score_value = score_value
        self.timer = 3.0  # Плавающие очки остаются видимыми 3 секунды

    def draw(self, surface):
        draw_text(f"+{self.score_value}", large_font, (255, 255, 0), surface, self.x, self.y)
        self.y -= 0.5  # Очки будут подниматься медленнее
        self.timer -= 0.03  # Замедляем исчезновение очков

# Функция для выбора сложности
def choose_difficulty():
    choosing = True
    while choosing:
        screen.fill((0, 0, 0))
        draw_text("Выберите сложность:", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100)
        draw_text("1. Легкий", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("2. Средний", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60)
        draw_text("3. Сложный", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)
        pygame.display.update()

        # Получаем координаты мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Проверка нажатия мыши по кнопкам
        if pygame.mouse.get_pressed()[0]:
            if SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100:
                if SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 50:
                    return 1  # Легкий
                elif SCREEN_HEIGHT // 2 + 60 <= mouse_y <= SCREEN_HEIGHT // 2 + 110:
                    return 2  # Средний
                elif SCREEN_HEIGHT // 2 + 120 <= mouse_y <= SCREEN_HEIGHT // 2 + 170:
                    return 3  # Сложный

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1  # Легкий
                if event.key == pygame.K_2:
                    return 2  # Средний
                if event.key == pygame.K_3:
                    return 3  # Сложный

# Функция для перезапуска игры
def restart_game():
    global difficulty, target_speed_x, target_speed_y, target_x, target_y, score, start_time
    difficulty = choose_difficulty()
    score = 0
    start_time = time.time()
    set_speed()

# Установка скорости мишени в зависимости от сложности
def set_speed():
    global target_speed_x, target_speed_y
    if difficulty == 1:  # Легкий
        target_speed_x = random.choice([-0.3, 0.3]) * (SCREEN_WIDTH / 600)  # Уменьшили базовое значение
        target_speed_y = random.choice([-0.3, 0.3]) * (SCREEN_HEIGHT / 400)  # Уменьшили базовое значение
    elif difficulty == 2:  # Средний
        target_speed_x = random.choice([-0.6, 0.6]) * (SCREEN_WIDTH / 600)
        target_speed_y = random.choice([-0.6, 0.6]) * (SCREEN_HEIGHT / 400)
    else:  # Сложный
        target_speed_x = random.choice([-1, 1]) * (SCREEN_WIDTH / 600)
        target_speed_y = random.choice([-1, 1]) * (SCREEN_HEIGHT / 400)


# Функция для отображения экрана с предложением продолжить или выйти
def end_game_screen():
    screen.fill((0, 0, 0))
    draw_text("Хотите продолжить?", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 200,
              SCREEN_HEIGHT // 2 - 100)
    draw_text("Y - Продолжить", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("N - Выйти", font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60)
    pygame.display.update()

    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Если пользователь хочет продолжить
                    restart_game()
                    choosing = False
                if event.key == pygame.K_n:  # Если пользователь хочет выйти
                    pygame.quit()
                    exit()

# Выбор уровня сложности
difficulty = choose_difficulty()
set_speed()

# Функция обратного отсчёта
def countdown():
    for i in range(3, 0, -1):  # Обратный отсчёт с 3 до 1
        screen.fill((0, 0, 0))  # Чёрный фон
        draw_text(str(i), font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)
        pygame.display.update()
        time.sleep(1)  # Пауза на 1 секунду перед каждым числом

# Позиция мишени
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

message = ""

# Обратный отсчёт перед началом игры
countdown()  # Добавляем обратный отсчёт

# Основной игровой цикл
running = True
while running:
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(game_time - elapsed_time))

    if remaining_time == 0:
        message = f"Время вышло! Очки: {score}"

        # Проигрываем звук окончания игры
        pygame.mixer.Sound.play(end_game_sound)

        draw_text(message, font, (255, 255, 255), screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2)
        pygame.display.update()
        time.sleep(3)
        end_game_screen()  # Вызов экрана для выбора: продолжить или выйти

    # Отрисовка фона
    screen.blit(background_img, (0, 0))

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                score += 1
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                pygame.mixer.Sound.play(hit_sound)
                is_flashing = True
                flash_timer = flash_duration
                floating_scores.append(FloatingScore(mouse_x, mouse_y, 1))
            else:
                pygame.mixer.Sound.play(miss_sound)

    # Движение мишени
    target_x += target_speed_x
    target_y += target_speed_y

    if target_x <= 0 or target_x + target_width >= SCREEN_WIDTH:
        target_speed_x = -target_speed_x
    if target_y <= 0 or target_y + target_height >= SCREEN_HEIGHT:
        target_speed_y = -target_speed_y

    if is_flashing:
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surface.set_alpha(128)
        flash_surface.fill((255, 255, 255))
        screen.blit(flash_surface, (0, 0))
        flash_timer -= 0.05
        if flash_timer <= 0:
            is_flashing = False

    # Отрисовываем мишень
    screen.blit(target_img, (target_x, target_y))

    # Отрисовываем плавающие очки
    for floating_score in floating_scores[:]:
        floating_score.draw(screen)
        if floating_score.timer <= 0:
            floating_scores.remove(floating_score)

    # Отрисовываем сообщение
    if message:
        draw_text(message, font, (255, 255, 255), screen, 10, 10)

    # Отрисовываем счёт
    draw_text(f"Очки: {score}", font, (255, 255, 255), screen, 10, 60)

    # Отрисовываем таймер
    draw_text(f"Время: {remaining_time}", font, (255, 255, 255), screen, 10, 110)

    # Отрисовываем инструкцию для выхода в меню
    draw_text("Нажмите 'R' для выхода в меню", small_font, (255, 255, 255), screen, 10, SCREEN_HEIGHT - 40)

    # Обновляем экран
    pygame.display.update()

pygame.quit()
