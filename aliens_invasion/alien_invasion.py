import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group

def run_game():
    pygame.init()
    game_settings = Settings()

    """ Set screen size. """
    screen = pygame.display.set_mode((
        game_settings.screen_width, 
        game_settings.screen_heigh
    ))
    pygame.display.set_caption("Aliens Invasion")

    """ Make a ship. """
    ship = Ship(game_settings, screen)

    bullets = Group()

    while True:
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        gf.update_screen(game_settings, screen, ship, bullets)

run_game()