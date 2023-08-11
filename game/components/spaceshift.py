from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

class Spaceshift(Sprite):
    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (40,60))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - 40
        self.rect.y = 500

    def update(self, user_input):
        if user_input[pygame.K_LEFT]:
            self.move_left()
        elif user_input[pygame.K_RIGHT]:
            self.move_right()
        elif user_input[pygame.K_UP]:
            self.move_up()
        elif user_input[pygame.K_DOWN]:
            self.move_down()

    def draw(self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))

    def move_left(self):
        if self.rect.x <= -40:
            self.rect.x += SCREEN_WIDTH + 40
        else:
            self.rect.x -= 10

    def move_right(self):
        if self.rect.x >= SCREEN_WIDTH - 10:
            self.rect.x -= SCREEN_WIDTH + 30
        else:
            self.rect.x += 10

    def move_up(self):
        if self.rect.y >= 10:
            self.rect.y -= 10

    def move_down(self):
        if self.rect.y <= 530:
            self.rect.y += 10