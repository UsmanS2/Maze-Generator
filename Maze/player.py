import pygame

turtle = pygame.image.load("turtle.png")
turtle = pygame.transform.smoothscale(turtle, [25,25])
turtle = pygame.transform.flip(turtle, True, False)

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.image = turtle
    self.rect = self.image.get_rect()
    self.rect.w = self.image.get_rect()[2] - 24
    self.rect.h = self.image.get_rect()[3] - 24
    self.rect.x = x
    self.rect.y = y
    self.changeX = 0
    self.changeY = 0

  def update(self):
    self.rect.x += self.changeX
    self.rect.y += self.changeY