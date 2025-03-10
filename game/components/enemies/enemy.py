import random
import pygame
from pygame.sprite import Sprite
from game.components.bullets.bullet import Bullet

from game.utils.constants import DEFAULT_TYPE, ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(Sprite):
    SHIP_WIDTH = 60
    SHIP_HEIGHT = 80
    Y_POS = 10
    X_POS = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_Y = [1,2,3]
    SPEED_X = [5,10,15,20]
    MOV_X = {0: 'left', 1:'right'}
    ENEMIES = [ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4]
    
    def __init__(self):
        self.image = self.ENEMIES[random.randint(0,3)]
        self.image = pygame.transform.scale(self.image,(self.SHIP_WIDTH, self.SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.y = self.Y_POS
        self.rect.x = self.X_POS[random.randint(0,10)]
        self.speed_x = self.SPEED_X[random.randint(0,3)]
        self.speed_y = self.SPEED_Y[random.randint(0,2)]
        self.movement_x = self.MOV_X[random.randint(0,1)]
        self.move_x_for = random.randint(30, 100)
        self.index = 0
        self.shooting_time = random.randint(30, 50)
        self.type = 'enemy'
        self.has_power_up = False
        self.power_up_type = DEFAULT_TYPE

    def update(self, ships, game):
        self.rect.y += self.speed_y
        self.shoot(game.bullet_manager)

        if self.movement_x == 'left':
            self.rect.x -= self.speed_x
        else:
            self.rect.x += self.speed_x
        
        self.change_movement_x()

        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def change_movement_x(self):
        self.index += 1
        
        if (self.index >= self.move_x_for and self.movement_x == 'right') or (self.rect.x >= SCREEN_WIDTH - self.SHIP_WIDTH):
            self.movement_x = 'left'
            self.move_x_for = random.randint(30, 100)
            self.index = 0
        elif (self.index >= self.move_x_for and self.movement_x == 'left') or (self.rect.x <=10):
            self.movement_x = 'right'
            self.move_x_for = random.randint(30, 100)
            self.index = 0

    def shoot(self, bullet_manager):
        current_time = pygame.time.get_ticks()
        if self.shooting_time <= current_time:
            bullet = Bullet(self)
            bullet_manager.add_bullet(bullet)
            self.shooting_time += random.randint(30, 50)