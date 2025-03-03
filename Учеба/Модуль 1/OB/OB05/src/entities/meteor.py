import pygame
import random

class Meteor:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = random.randint(30, 60)
        self.original_image = pygame.image.load("assets/images/meteor.png")
        # В классе Meteor:
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        # Меньше размер -> больше скорость
        if 1+(60 - self.size) > 2:
            self.speed = 1+(60 - self.size)
        else: self.speed = 1+(60 - self.size) / 5
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.size)
        self.rect.y = -self.size

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed

