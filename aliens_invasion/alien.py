import pygame
from pygame.sprite import AbstractGroup, Sprite
from pygame import Surface

from settings import Settings

class Alien(Sprite):

    def __init__(self,
        settings: Settings,
        screen: Surface,
        *groups: AbstractGroup
        ) -> None:
        super().__init__(*groups)
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("images/alien.png")
        self.image = pygame.transform.smoothscale(
            self.image,
            (80, 80)
        )
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)