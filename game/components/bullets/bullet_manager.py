import pygame

from pygame import mixer
from game.utils.constants import SHIELD_TYPE

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.enemy_bullets = []

    def update(self, game):
        
        for bullet in self.enemy_bullets:
            bullet.update(self.enemy_bullets)         
            if bullet.rect.colliderect(game.player.rect) and bullet.owner == 'enemy':
                if game.player.power_up_type != SHIELD_TYPE:
                    game.live_count -= 1
                    if game.live_count < 0:
                        game.death_count += 1
                        game_over_sound = mixer.Sound('game/assets/Sound/game_over.mp3')
                        game_over_sound.set_volume(0.1)
                        game_over_sound.play()
                        game.playing = False
                        pygame.time.delay(4000)
                        break
                self.enemy_bullets.remove(bullet)

        for bullet in self.bullets:
            bullet.update(self.bullets)
            for enemy in game.enemy_manager.enemies:
                if bullet.rect.colliderect(enemy.rect) and bullet.owner == 'player':
                    explosion_sound = mixer.Sound('game/assets/Sound/explosion.wav')
                    explosion_sound.set_volume(0.1)
                    explosion_sound.play()   
                    game.enemy_manager.enemies.remove(enemy)
                    game.score += 100
                    self.bullets.remove(bullet)

    def draw(self, screen):
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

    def add_bullet(self, bullet):
        if bullet.owner == 'enemy' and len (self.enemy_bullets) < 1:
            self.enemy_bullets.append(bullet)
        elif bullet.owner == 'player' and len (self.bullets) < 3:
            self.bullets.append(bullet)

    def reset(self):
        self.bullets = []
        self.enemy_bullets = []