import pygame

from settings import Settings
from ship import Ship

class Bullet(pygame.sprite.Sprite):

    def __init__(self, settings: Settings, screen: pygame.Surface, ship: Ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_heigh)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

        self.image = pygame.Surface(
            (settings.bullet_width, settings.bullet_heigh)
        )
        self.image.fill(self.color)

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = int(self.y)

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)