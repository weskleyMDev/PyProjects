import pygame
import game_functions as gf
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien

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
    aliens = Group()

    gf.create_fleet(game_settings, screen, aliens)

    while True:
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(game_settings, screen, ship, aliens, bullets)

run_game()