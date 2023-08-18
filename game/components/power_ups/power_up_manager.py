import random
import pygame
from game.components.power_ups.heart import Heart
from game.components.power_ups.increased_bullets import IncreasedBullet

from game.components.power_ups.shield import Shield
from game.utils.constants import BULLET_TYPE, HEART_TYPE, SHIELD_TYPE, SPACESHIP_SHIELD

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.duration = random.randint(3000, 5000)
        self.when_appers = random.randint(5000, 10000)

    def update(self, game):
        current_time = pygame.time.get_ticks()
        if len(self.power_ups) == 0 and current_time >= self.when_appers:
            self.generate_power_up()

        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)

            if game.player.rect.colliderect(power_up.rect) and power_up.type == SHIELD_TYPE:
                power_up.start_time = pygame.time.get_ticks()
                game.player.power_up_type = power_up.type
                game.player.has_power_up = True
                game.player.power_time_up = power_up.start_time + self.duration
                game.player.set_image((80,100), SPACESHIP_SHIELD)
                self.power_ups.remove(power_up)

            if game.player.rect.colliderect(power_up.rect) and power_up.type == HEART_TYPE and game.live_count < 3:
                game.live_count += 1
                self.power_ups.remove(power_up)

            if game.player.rect.colliderect(power_up.rect) and power_up.type == BULLET_TYPE:
                power_up.start_time = pygame.time.get_ticks()
                game.player.power_up_type = power_up.type
                game.player.has_power_up = True
                game.player.power_time_up = power_up.start_time + self.duration
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def generate_power_up(self):
        power_available = [Heart(), Shield() ,IncreasedBullet()]
        power_up = power_available[random.randint(0,2)]
         
        self.when_appers += random.randint(5000, 10000)
        self.power_ups.append(power_up)

    def reset(self):
        self.power_ups = []