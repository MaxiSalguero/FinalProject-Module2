from pygame.sprite import Sprite
from game.components.bullets.bullet import Bullet
from game.utils.constants import DEFAULT_TYPE, SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT
from pygame import mixer
import pygame

class Spaceshift(Sprite):
    SHIP_SPEED = 10
    SHIP_WIDTH = 60
    SHIP_HEIGHT = 80
    X_POS = (SCREEN_WIDTH // 2) - SHIP_WIDTH
    Y_POS = 500
    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (self.SHIP_WIDTH,self.SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - 40
        self.rect.y = 500
        self.type = 'player'
        self.power_up_type = DEFAULT_TYPE
        self.has_power_up = False
        self.power_time_up = 0

    def update(self, user_input, game):
        if user_input[pygame.K_SPACE]:
            self.shoot(game)
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
        if self.rect.y <= 500:
            self.rect.y += 10

    def shoot(self, game):
        bullet = Bullet(self)
        game.bullet_manager.add_bullet(bullet)
        bullet_sound = mixer.Sound('game/assets/Sound/laser.wav')
        bullet_sound.set_volume(0.1)
        bullet_sound.play()

    def set_image(self, size = (SHIP_WIDTH, SHIP_HEIGHT), image = SPACESHIP):
        self.image = image
        self.image = pygame.transform.scale(self.image ,size)

    def reset(self):
        self.rect.x = (SCREEN_WIDTH // 2) - 40
        self.rect.y = 500