import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen

        #加载外星人的图像并设置其rect属性
        self.image = pygame.image.load('Alien_attack game/images/alien.bmp')
        self.image = pygame.transform.scale(self.image,(80,60))
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings

        #将外星人放置在屏幕左上角
        self.rect.x = self.rect.width/2
        self.rect.y = self.rect.height/2      #将外星人的左边距和上边距分别设置为外星人的宽度和高度

        #存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        #向右移动外星人
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x