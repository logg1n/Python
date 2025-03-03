# Добавляем в начало кода
import pygame


class Button:
   def __init__(self, text, x, y, width, height, action=None):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = (50, 50, 50)
      self.hover_color = (100, 100, 100)
      self.text = text
      self.action = action
      self.font = pygame.font.Font(None, 36)

   def draw(self, screen):
      mouse_pos = pygame.mouse.get_pos()
      color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

      pygame.draw.rect(screen, color, self.rect)
      text_surf = self.font.render(self.text, True, (255, 255, 255))
      text_rect = text_surf.get_rect(center=self.rect.center)
      screen.blit(text_surf, text_rect)

   def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
         if self.rect.collidepoint(event.pos):
            if self.action:
               self.action()  # Должно вызывать quit_game()
            return True
      return False