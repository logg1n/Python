# Класс анимации взрыва
import pygame


class Explosion:
   def __init__(self, position):
      self.sheet = pygame.image.load("assets/images/explosion.png").convert_alpha()
      self.frames = []
      self.frame_size = 64
      self.columns = 3

      # Нарезка спрайт-листа
      for i in range(9):
         x = (i % self.columns) * self.frame_size
         y = (i // self.columns) * self.frame_size
         frame = self.sheet.subsurface((x, y, self.frame_size, self.frame_size))
         self.frames.append(frame)

      self.current_frame = 0
      self.image = self.frames[self.current_frame]
      self.rect = self.image.get_rect(center=position)
      self.last_update = pygame.time.get_ticks()

   def update(self):
      now = pygame.time.get_ticks()
      if now - self.last_update > 50:
         self.last_update = now
         self.current_frame += 1
         if self.current_frame >= len(self.frames):
            return False
         self.image = self.frames[self.current_frame]
      return True

