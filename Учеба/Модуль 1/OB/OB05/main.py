import pygame
import sys

from src.entities.button import Button
from src.entities.explosion import Explosion
from src.entities.player import Player
from src.entities.meteor import Meteor
import os


HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
   try:
      if os.path.exists(HIGH_SCORE_FILE):
         with open(HIGH_SCORE_FILE, "r") as f:
            content = f.read().strip()
            # Проверка на пустоту и цифры
            if content.isdigit():
               return int(content)
      return 0  # Если файл не существует или данные некорректны
   except Exception as e:
      print(f"Ошибка загрузки рекорда: {e}")
      return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except:
        pass

# Инициализация Pygame
pygame.init()

# Настройки окна
window_width = 500
window_height = 700
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Космические защитники")

# Шрифты
pygame.font.init()
try:
   score_font = pygame.font.Font("assets/fonts/retro.ttf", 36)
except:
   score_font = pygame.font.Font(None, 36)

# Звуки
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
try:
   pygame.mixer.music.load("assets/sounds/background.mp3")
   pygame.mixer.music.set_volume(0.1)
   pygame.mixer.music.play(-1)
   shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
   explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
   shoot_sound.set_volume(0.3)
   explosion_sound.set_volume(0.7)
except Exception as e:
   print(f"Ошибка загрузки ресурсов: {e}")
   shoot_sound = None
   explosion_sound = None

# Графика
try:
   background = pygame.image.load("assets/images/background.jpg").convert()
   background = pygame.transform.scale(background, (window_width, window_height))
except FileNotFoundError:
   background = pygame.Surface((window_width, window_height))
   background.fill((0, 0, 0))


# Состояния игры
class GameState:
   MAIN_MENU = 0
   PLAYING = 1
   GAME_OVER = 2


# Инициализация игровых объектов
def game_reset():
   global player, meteors, score, explosions, meteor_timer, high_score, score
   player = Player(screen, 5)
   player.shoot_sound = shoot_sound
   meteors = []
   explosions = []
   score = 0
   meteor_timer = 0
   high_score = load_high_score()
   score = 0

game_reset()


# Создаем кнопки
def start_game():
   global current_state
   current_state = GameState.PLAYING


def quit_game():
   pygame.quit()
   sys.exit()

menu_buttons = [
    Button("Start Game", 150, 200, 200, 50, start_game),
    Button("Quit", 150, 300, 200, 50, lambda: (pygame.quit(), sys.exit()))
]
current_state = GameState.MAIN_MENU

game_over_buttons = [
    Button("Restart", 150, 400, 200, 50, lambda: [game_reset(), set_current_state(GameState.PLAYING)]),
    Button("Main Menu", 150, 480, 200, 50, lambda: set_current_state(GameState.MAIN_MENU)),
    Button("Quit", 150, 560, 200, 50, quit_game)
]

def set_current_state(state):
   global current_state
   current_state = state

clock = pygame.time.Clock()
running = True

# Основной игровой цикл
while running:
   # Обработка событий для всех состояний
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

      # Обработка для всех состояний
      if current_state == GameState.MAIN_MENU:
         for button in menu_buttons:
            button.handle_event(event)

      elif current_state == GameState.GAME_OVER:
         for button in game_over_buttons:
            button.handle_event(event)

      # Обработка клавиши R для рестарта
      if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
         if current_state == GameState.GAME_OVER:
            game_reset()
            set_current_state(GameState.PLAYING)

   # Обновление игры
   screen.blit(background, (0, 0))

   if current_state == GameState.MAIN_MENU:
      high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 0))
      screen.blit(high_score_text, (window_width // 2 - 100, 150))
      for button in menu_buttons:
         button.draw(screen)

   elif current_state == GameState.PLAYING:
      dt = clock.tick(60)
      keys = pygame.key.get_pressed()

      # Управление игроком
      player.update(keys)

      # Генерация метеоритов
      meteor_timer += 1
      if meteor_timer >= 30:
         meteors.append(Meteor(window_width, window_height))
         meteor_timer = 0

      # Обновление метеоритов
      for meteor in meteors[:]:
         meteor.update()
         if meteor.rect.top > window_height:
            meteors.remove(meteor)

      # Проверка столкновений пуль
      bullets_to_remove = []
      meteors_to_remove = []

      for bullet in player.bullets[:]:
         bullet.update()
         if bullet.rect.bottom < 0:
            bullets_to_remove.append(bullet)
            continue

         for meteor in meteors[:]:
            if bullet.rect.colliderect(meteor.rect):
               bullets_to_remove.append(bullet)
               meteors_to_remove.append(meteor)
               score += max(150 - meteor.size, 50)
               explosions.append(Explosion(meteor.rect.center))
               if explosion_sound:
                  explosion_sound.play()

      # Проверка столкновений игрока
      # Проверка столкновения игрока с метеоритами
      collision = False
      for meteor in meteors[:]:  # Используем копию списка
         if player.rect.colliderect(meteor.rect):
            # Уничтожаем метеорит и игрока
            meteors.remove(meteor)
            explosions.append(Explosion(player.rect.center))
            explosions.append(Explosion(meteor.rect.center))
            collision = True

      if collision:
         current_state = GameState.GAME_OVER
         if score > high_score:
            high_score = score
            save_high_score(high_score)
         if explosion_sound:
            explosion_sound.play()
         continue  # Прекращаем обработку кадра

      # Удаление объектов
      for bullet in bullets_to_remove:
         if bullet in player.bullets:
            player.bullets.remove(bullet)

      for meteor in meteors_to_remove:
         if meteor in meteors:
            meteors.remove(meteor)

      # Отрисовка игровых объектов
      player.draw()
      for meteor in meteors:
         meteor.draw(screen)

      # Отрисовка интерфейса
      screen.blit(score_font.render(f"SCORE: {score}", True, (255, 255, 255)), (10, 10))

   elif current_state == GameState.GAME_OVER:
      # Текст
      screen.blit(score_font.render("GAME OVER", True, (255, 0, 0)),
                  (window_width // 2 - 100, window_height // 2 - 100))
      screen.blit(score_font.render(f"Score: {score}", True, (255, 255, 255)),
                  (window_width // 2 - 80, window_height // 2 - 40))
      screen.blit(score_font.render(f"Record: {high_score}", True, (255, 215, 0)),
                  (window_width // 2 - 90, window_height // 2 + 20))

      # Кнопки
      for button in game_over_buttons:
         button.draw(screen)
   # Обновление анимаций
   explosions = [e for e in explosions if e.update()]
   for explosion in explosions:
      screen.blit(explosion.image, explosion.rect)

   pygame.display.flip()

pygame.quit()
sys.exit()