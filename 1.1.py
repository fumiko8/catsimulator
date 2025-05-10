import pygame
import random
from PIL import Image
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1200, 675 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_RED = (255, 203, 219)
DARK_PINK = (161, 96, 161)
DARK_BACLAJAN = (68, 26, 47)
LIGHT_PINK = (182, 140, 149)
PEACH = (238, 152, 101)
YELLOW = (249, 192, 131)
ABRICOT = (252, 218, 182)
FONT_COLOR = WHITE
DIALOG_BG_COLOR = (240, 127, 127, 180)  # прозрачный красный (RGBA)
BORDER_COLOR = (200, 30, 30)
BORDER_THICKNESS = 4
TEXT_COLOR_NORMAL = WHITE
TEXT_COLOR_HOVER = (240, 127, 127)  # светло-розовый или любой другой цвет при наведении
TEXT_COLOR_PRESSED = (214, 51, 52)  # цвет при нажатии



# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Симулятор кота")

# Загрузка изображения фона
image = pygame.image.load("newroom.jpg")

foreground = pygame.image.load("siamese.png")
# Set the size for the image
DEFAULT_IMAGE_SIZE = (200, 200)
# Scale the image to your needed size
foreground = pygame.transform.scale(foreground, DEFAULT_IMAGE_SIZE)
# для перемещения
foreground.convert()
rect = foreground.get_rect()
rect.center = WIDTH//2.15, HEIGHT//1.25


 
# Шрифт
font = pygame.font.Font(None, 36)


# Load and define button images. Three states normal, hover, and pressed
normal = pygame.image.load('normal.png')
hover = pygame.image.load('hover.png')
pressed = pygame.image.load('pressed.png')
DEFAULT_BUTTON_SIZE = (310, 80)
# Scale the image to your needed size
normal = pygame.transform.scale(normal, DEFAULT_BUTTON_SIZE)
hover = pygame.transform.scale(hover, DEFAULT_BUTTON_SIZE)
pressed = pygame.transform.scale(pressed, DEFAULT_BUTTON_SIZE)
# change cursor on hover
hand = pygame.SYSTEM_CURSOR_HAND
 
# Create Button class
class Button:
    def __init__(self, image, pos, callback):
        '''
            Create a animated button from images
            self.callback is for a funtion for the button to do - set to None
        '''
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.callback = callback
 
 
    # Define function for normal button state
    def normal(self):
        self.image = normal
        pygame.mouse.set_cursor()
 
    # Define function for mouse hover state
    def hover(self):
        self.image = hover
        pygame.mouse.set_cursor(hand)
 
    # Define function for pressed state
    def pressed(self):
        self.image = pressed

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.callback:
                self.callback()  # Вызов функции обратного вызова
                

# Игровые данные
inventory = [] 
available_actions = ["Осмотреться", "Положить обратно"]
level_parameters = (
    (1, "Уровень 1", 5),
    (2, "Уровень 2", 8),
    (3, "Уровень 3", 10)
)
completed_quests = set()
item_descriptions = {
    "мышка": "Игрушечная мышка, которая тихо шуршит.",
    "носки": "Обычные носки, хозяин вечно бросает вещи где попало.",
    "попрыгунчик": "Маленький игрушечный мячик, которым весело играть.",
    "миска": "Железная миска на подставке.",
    "тапки": "Тапки хозяина."
}
levels = {
    1: {"name": "Уровень 1", "tasks": ["Собрать 5 игрушек"]},
    2: {"name": "Уровень 2", "tasks": ["Собрать 8 игрушек"]},
    3: {"name": "Уровень 3", "tasks": ["Собрать 10 игрушек"]}
}
player_stats = {
    "Имя": "Мурлыка",
    "Настроение": 100,
    "Уровень": 1,
    "Опыт": 0
}



# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Функция для проверки выполнения уровня
def check_level_completion():
    required_toys = levels[player_stats['Уровень']]["tasks"][0].split()[1]
    if len(inventory) >= int(required_toys):
        print(f"Поздравляем! Вы завершили уровень {levels[player_stats['Уровень']]['name']}!")
        completed_quests.add(levels[player_stats['Уровень']]['name'])
        player_stats['Уровень'] += 1
        inventory.clear()
        if player_stats['Уровень'] > len(levels):
            print("Вы завершили все уровни! Игра окончена.")
            return True
    return False

# Основной игровой цикл
running = True
moving = False

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# Функция для отображения текста поочередно
def display_text_sequence(text, delay_ms):
    clock = pygame.time.Clock()
    for i in range(1, len(text) + 1):
        yield text[:i]
        # Вместо time.sleep, задержка будет контролироваться в основном цикле
        # здесь вызываем только yield, delay будет реализован в основном цикле

# Функция для рисования диалогового окна с прозрачным фоном и рамкой
def draw_dialog_box(surface, rect, bg_color, border_color, border_thickness):
    # Создаем прозрачную поверхность для диалогового окна с альфа-каналом
    dialog_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Полупрозрачный бэкграунд
    pygame.draw.rect(dialog_surf, bg_color, dialog_surf.get_rect(), border_radius=12)
    
    # Рисуем рамку - много небольших прямоугольников для красивой рамки
    pygame.draw.rect(dialog_surf, border_color, dialog_surf.get_rect(), border_thickness, border_radius=12)

    # Копируем диалоговую поверхность на основной экран
    surface.blit(dialog_surf, rect.topleft)



# Параметры диалогового окна
dialog_width = WIDTH - 100
dialog_height = 100
dialog_x = 50
dialog_y = HEIGHT - dialog_height - 30
dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
# Текст и управление для показа по буквам
text_sequence = "Мяу мяу мяу, нужно собрать все игрушки"
text_delay_ms = 50  # задержка между буквами в миллисекундах
running = True
start_time = pygame.time.get_ticks()
show_text = False
text_generator = None
current_text = ""
last_update_time = 0

while running:
    current_time = pygame.time.get_ticks()
    screen.fill(WHITE)

    # Получаем текущие размеры окна
    current_width, current_height = screen.get_size()

    # Изменяем размер изображения в соответствии с размерами окна
    scaled_image = pygame.transform.scale(image, (current_width, current_height))

    # Отрисовка изображения
    screen.blit(scaled_image, (0, 0))

    # Отрисовка foreground
    screen.blit(foreground, rect)

    # Отображение статуса игрока
    draw_text(f"Имя: {player_stats['Имя']}", font, WHITE, screen, 20, 20)
    draw_text(f"Настроение: {player_stats['Настроение']}", font, WHITE, screen, 20, 60)
    draw_text(f"Уровень: {player_stats['Уровень']}", font, WHITE, screen, 20, 100)
    draw_text(f"Инвентарь: {inventory}", font, WHITE, screen, 20, 140)
    draw_text(f"Задания: {levels[player_stats['Уровень']]['tasks']}", font, WHITE, screen, 20, 180)

    # Создание кнопок
    button_width, button_height = 300, 50
    for i, action in enumerate(available_actions):
        button_rect = pygame.Rect(45, 230 + i * (button_height + 20), button_width, button_height)
        
        draw_text(action, font, WHITE, screen, button_rect.x + 10, button_rect.y + 10)

    # Проверка времени для начала отображения текста через 5 секунд
    if not show_text and current_time - start_time > 800:
        show_text = True
        text_generator = display_text_sequence(text_sequence, text_delay_ms)
        last_update_time = current_time
    
    # Отрисовка диалогового окна и текста
    if show_text:
        # Обновляем текст по задержке
        if current_time - last_update_time > text_delay_ms and text_generator is not None:
            try:
                current_text = next(text_generator)
            except StopIteration:
                text_generator = None
            last_update_time = current_time
        # Нарисовать диалоговое окно с рамкой
        draw_dialog_box(screen, dialog_rect, DIALOG_BG_COLOR, BORDER_COLOR, BORDER_THICKNESS)
        # Позиция текста внутри диалогового окна с небольшой отступ
        text_x = dialog_rect.x + 20
        text_y = dialog_rect.y + dialog_height // 3
        draw_text(current_text, font, FONT_COLOR, screen, text_x, text_y)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
    

        if event.type == pygame.KEYDOWN:

             if event.key == pygame.K_ESCAPE:
              running = False
        
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
    


            for i, action in enumerate(available_actions):
                button_rect = pygame.Rect(20, 250 + i * (button_height + 10), button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    if action == "Осмотреться":
                        toy = random.choice(["мышка", "носки", "попрыгунчик", "миска", "тапки"])
                        inventory.append(toy)
                        print(f"Вы собрали {toy}.")
                   
                    elif action == "Положить обратно":
                        if inventory:
                            item = inventory.pop(0)
                            print(f"Положили обратно {item}.")
                        else:
                            print("Инвентарь пуст.")
            
                    # Проверка выполнения уровня
                    if check_level_completion():
                        running = False
        
            if rect.collidepoint(event.pos):
              moving = True
        elif event.type == MOUSEBUTTONUP:          
            moving = False
        elif event.type == MOUSEMOTION and moving:
            rect.move_ip(event.rel)


    # Create a button from the Button class with args for state, position, and callback
    button_look = Button(normal, (45, 230), None)  # Кнопка "Осмотреться"
    button_put_back = Button(normal, (45, 300), None)  # Кнопка "Положить обратно"
 
    # Get mouse button from pygame
    left, middle, right = pygame.mouse.get_pressed()
 
    # If cursor is over button change state to hover else state is normal
    if button_look.rect.collidepoint(pygame.mouse.get_pos()):
        button_look.hover()
 
        # If left mouse button pressed change state to pressed else hover
        if left and button_look.rect.collidepoint(pygame.mouse.get_pos()):
            button_look.pressed()
            text_color = TEXT_COLOR_PRESSED
        else:
            button_look.hover()
            text_color = TEXT_COLOR_HOVER
    else:
        button_look.normal()
        text_color = TEXT_COLOR_NORMAL

    if button_put_back.rect.collidepoint(pygame.mouse.get_pos()):
        button_put_back.hover()
 
        # If left mouse button pressed change state to pressed else hover
        if left and button_put_back.rect.collidepoint(pygame.mouse.get_pos()):
            button_put_back.pressed()
            text_color_put_back = TEXT_COLOR_PRESSED
        else:
            button_put_back.hover()
            text_color_put_back = TEXT_COLOR_HOVER
    else:
        button_put_back.normal()
        text_color_put_back = TEXT_COLOR_NORMAL
    
    

    # Отрисовка кнопки
    screen.blit(button_look.image, button_look.rect)
    draw_text("Осмотреться", font, text_color, screen, button_look.rect.x + 75, button_look.rect.y + 25)

    screen.blit(button_put_back.image, button_put_back.rect)
    draw_text("Положить обратно", font, text_color_put_back, screen, button_put_back.rect.x + 45, button_put_back.rect.y + 25)

    # Обновление экрана
    pygame.display.update()

# Завершение Pygame
pygame.quit()
