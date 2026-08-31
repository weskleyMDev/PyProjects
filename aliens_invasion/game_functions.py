import sys
import pygame

from ship import Ship
from settings import Settings
from bullet import Bullet

def check_events(settings: Settings, screen: pygame.Surface, ship: Ship, bullets: pygame.sprite.Group):
    """ Keyword and mouse events. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            

def check_keydown_events(
    event: pygame.event.Event,
    settings: Settings,
    screen: pygame.Surface,
    ship: Ship,
    bullets: pygame.sprite.Group
):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(settings: Settings, screen: pygame.Surface, ship: Ship,
    bullets: pygame.sprite.Group):
    """ Update images and flip to the new screen. """
    screen.fill(settings.bg_color)

    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    
    pygame.display.flip()