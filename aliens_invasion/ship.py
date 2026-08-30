import pygame


class Ship:
    """ A class of rocket ship. """

    def __init__(self, screen: pygame.Surface):
        """ Initialize the ship and set its starting position. """
        self.screen = screen

        """ Load the ship image and get its rect. """
        self.image = pygame.image.load("images/DurrrSpaceShip.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        """ Start each new ship at the same position. """
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        """ Movement flag """
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship at its current location. """
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right:
            self.rect.centerx += 1
        if self.moving_left:
            self.rect.centerx -= 1