import sys
import pygame

from ship import Ship
from settings import Settings

def check_events(ship: Ship):
    """ Keyword and mouse events. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            

def check_keydown_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(settings: Settings, screen: pygame.Surface, ship: Ship):
    """ Update images and flip to the new screen. """
    screen.fill(settings.bg_color)
    ship.blitme()
    
    pygame.display.flip()