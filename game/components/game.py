import pygame

from pygame import mixer
from game.components.bullets.bullet_manager import BulletManager
from game.components.enemies.enemy_manager import EnemyManager
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import PowerUpManager
from game.components.spaceshift import Spaceshift

from game.utils.constants import BG, BG_2, ENEMY_2, ENEMY_3, ENEMY_4, FONT_STYLE, HEART, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAME_OVER

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceshift()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.score = 0
        self.death_count = 0
        self.live_count = [3,2,1]
        self.menu = Menu('Press any key to start...')
        self.power_up_manager = PowerUpManager()
        self.top_score = []

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                mixer.music.pause()
                self.show_menu()
        pygame.display.quit()
        pygame.quit()    

    def run(self):
        self.score = 0
        self.live_count = 3
        self.player.reset()
        self.bullet_manager.reset()
        self.enemy_manager.reset()
        self.power_up_manager.reset()
        mixer.init()
        mixer.music.load('game/assets/Sound/background.wav')
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.draw_life()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def show_menu(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2

        self.menu.reset_screen_color(self.screen)

        if self.death_count > 0:
            game_over = pygame.transform.scale(GAME_OVER, (400, 120))
            score = self.score - 1
            self.top_score.append(score)
            top_score = max(self.top_score)
            self.screen.blit(game_over, (half_screen_width - 200, half_screen_height -100))
            self.menu.update_message(f'Final score: {score} | Top score: {top_score} | Deaths: {self.death_count}')
            
        icon_1 = pygame.transform.scale(ENEMY_3, (80, 120))
        icon_2 = pygame.transform.scale(ENEMY_4, (80, 120))   
        icon_3 = pygame.transform.scale(ICON, (80, 120))
        icon_4 = pygame.transform.scale(ENEMY_2, (80, 120)) 
        self.screen.blit(icon_4, (half_screen_width - 50, half_screen_height -250))
        self.screen.blit(icon_1, (half_screen_width + 100, half_screen_height -250))
        self.screen.blit(icon_2, (half_screen_width - 200, half_screen_height -250))
        self.screen.blit(icon_3, (half_screen_width - 50, half_screen_height + 20))
        self.menu.draw(self.screen)
        self.menu.update(self)

    def update_score(self):
        self.score += 1

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (255,255,255))
        text_rect = text.get_rect()
        text_rect.center = (90, SCREEN_HEIGHT - 30)
        self.screen.blit(text, text_rect)

    def draw_life(self):
        self.image = HEART
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect =  self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 60
        if self.live_count == 3:
            self.screen.blit(self.image,(self.rect.x - 140, self.rect.y))   
            self.screen.blit(self.image,(self.rect.x - 100, self.rect.y))
            self.screen.blit(self.image,(self.rect.x - 60, self.rect.y))
        elif self.live_count == 2:
            self.screen.blit(self.image,(self.rect.x - 140, self.rect.y))   
            self.screen.blit(self.image,(self.rect.x - 100, self.rect.y))
        elif self.live_count == 1:
            self.screen.blit(self.image,(self.rect.x - 140, self.rect.y))   

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 30)
                text = font.render(f'Power up enable for: {time_to_show} seconds', True, (255,255,255))
                self.screen.blit(text, (580, 10))
            else:
                self.player.has_power_up = False
                self.player.power_up_type = DEFAULT_TYPE
                self.player.set_image()