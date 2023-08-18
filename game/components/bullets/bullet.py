import pygame

from pygame.sprite import Sprite
from game.utils.constants import BULLET, BULLET_ENEMY, BULLET_TYPE, SCREEN_HEIGHT

class Bullet(Sprite):
    BULLET_SIZE = pygame.transform.scale(BULLET,(20,30))
    BULLET_ENEMY_SIZE = pygame.transform.scale(BULLET_ENEMY,(10,20))
    BULLETS = {'player': BULLET_SIZE, 'enemy':BULLET_ENEMY_SIZE}
    SPEED = 20

    def __init__(self, spaceshift):
        self.image = self.BULLETS[spaceshift.type]
        self.rect = self.image.get_rect()
        self.rect.center = spaceshift.rect.center
        self.owner = spaceshift.type
        self.owner_has_power = spaceshift.has_power_up
        self.owner_type_power = spaceshift.power_up_type

    def update(self, bullets):
        if self.owner == 'player':
            self.rect.y -= self.SPEED
        else:
            self.rect.y += self.SPEED
        
        if self.rect.y < 0 or self.rect.y >= SCREEN_HEIGHT:
            bullets.remove(self)

        if (self.owner == 'player') and (self.owner_has_power == True) and (self.owner_type_power == BULLET_TYPE):
            for bullet in bullets:
                self.set_image()

    def draw(self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))

    def set_image(self):
        BULLET_SIZE = pygame.transform.scale(BULLET,(40,60))
        self.image = BULLET_SIZE