import pygame
from settings import Settings


class Ship:
    """ A class of rocket ship. """

    def __init__(self, settings: Settings, screen: pygame.Surface):
        """ Initialize the ship and set its starting position. """
        self.screen = screen
        self.settings = settings

        """ Load the ship image and get its rect. """
        self.image = pygame.image.load("images/DurrrSpaceShip.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        """ Start each new ship at the same position. """
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        """ Store decimal value for ship's center """
        self.center = float(self.rect.centerx)

        """ Movement flag """
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship at its current location. """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update ship's center value, not the rect """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor

        """ Update rect object from self.center """
        self.rect.centerx = self.center