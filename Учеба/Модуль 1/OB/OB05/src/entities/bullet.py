import pygame


class Bullet:
   def __init__(self, x, y, speed):
      # Параметры движения
      self.speed = speed

      # Графические параметры
      self.width = 5
      self.height = 20
      self.color = (255, 255, 255)  # Основной цвет
      self.core_color = (255, 0, 0)  # Цвет ядра

      # Создание поверхности и прямоугольника
      self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
      self.rect = self.image.get_rect(center=(x, y))

      # Отрисовка пули
      self.image.fill(self.color)
      pygame.draw.line(self.image,
                       self.core_color,
                       (self.width // 2, 0),
                       (self.width // 2, self.height),
                       3)

   def update(self):
      """Обновление позиции пули"""
      self.rect.y -= self.speed

   def draw(self, screen):
      """Отрисовка пули на экране"""
      screen.blit(self.image, self.rect)