import sys
import pygame

from alien import Alien
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
        fire_bullet(settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event: pygame.event.Event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(settings: Settings, screen: pygame.Surface, ship: Ship, aliens: pygame.sprite.Group, bullets: pygame.sprite.Group):
    """ Update images and flip to the new screen. """
    screen.fill(settings.bg_color)

    bullets.draw(screen)
    aliens.draw(screen)
    ship.blitme()
    
    pygame.display.flip()

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(bullets: pygame.sprite.Group):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def create_fleet(settings: Settings, screen: pygame.Surface, aliens: pygame.sprite.Group):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    for alien_number in range(number_aliens_x):
        alien = Alien(settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)