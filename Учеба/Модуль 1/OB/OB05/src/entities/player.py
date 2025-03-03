import pygame
from .bullet import Bullet


class Player:
   def __init__(self, screen, speed, bullet_speed=10):
      self.screen = screen
      self.speed = speed
      self.bullet_speed = bullet_speed
      self.bullets = []

      # Загрузка изображения и получение прямоугольника
      self.original_image = pygame.image.load("assets/images/player.png").convert_alpha()
      # В классе Player:
      self.image = pygame.transform.scale(self.original_image, (50, 50))
      self.rect = self.image.get_rect()

      # Начальная позиция в центре нижней части экрана
      self.rect.center = (screen.get_width() // 2, screen.get_height() - 50)

      # Управление звуком
      self.shoot_sound = None

      # Параметры стрельбы
      self.shoot_delay = 300  # Задержка между выстрелами в миллисекундах
      self.last_shot = 0  # Время последнего выстрела

   # Остальные методы остаются без изменений
   def move_left(self):
      if self.rect.left > 0:
         self.rect.x -= self.speed

   def move_right(self):
      if self.rect.right < self.screen.get_width():
         self.rect.x += self.speed

   def draw(self):
      self.screen.blit(self.image, self.rect)
      for bullet in self.bullets:
         bullet.draw(self.screen)

   def shoot(self):
      """Создание пули с учетом задержки"""
      current_time = pygame.time.get_ticks()

      # Проверяем, прошло ли достаточно времени с последнего выстрела
      if current_time - self.last_shot >= self.shoot_delay:
         bullet_x = self.rect.centerx
         bullet_y = self.rect.top
         bullet = Bullet(bullet_x, bullet_y, 15)
         self.bullets.append(bullet)

         if self.shoot_sound:
            self.shoot_sound.play()

         # Обновляем время последнего выстрела
         self.last_shot = current_time

   def update(self, keys):
      """Обновление состояния с проверкой задержки"""
      # Движение
      if keys[pygame.K_LEFT]:
         self.move_left()
      if keys[pygame.K_RIGHT]:
         self.move_right()

      # Стрельба с автоматической перезарядкой
      if keys[pygame.K_SPACE]:
         self.shoot()  # Вызов метода с проверкой задержки

      # Обновление пуль
      for bullet in self.bullets[:]:
         bullet.update()
         if bullet.rect.bottom < 0:
            self.bullets.remove(bullet)
