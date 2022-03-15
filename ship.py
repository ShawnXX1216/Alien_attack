import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    #创建一个ship的类用于管理飞船的行为
    def __init__(self,ai_game):     #ai_game指向当前AlienInvasion实例的引用，便于访问AlienInvasion中定义的资源
        #初始化飞船及其位置
        super().__init__()
        self.screen = ai_game.screen        #将屏幕赋给ship的一个属性，便于这个类中的方法访问
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()        #将屏幕的属性rect赋给self.screen_rect，便于将飞船放置在屏幕的正确位置上

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('Alien_attack game/images/ship.bmp')     #父工作路径是python_work！！
        self.image = pygame.transform.scale(self.image,(80,60))         #把图片弄小点
        self.rect = self.image.get_rect()       #获取image的外接矩形

        #对于每艘新飞船，都将它放置在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性x中存储小数值  (因为rect的x属性只能存储整数值，所以要定义一个能存储数值的x属性)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #移动标志s
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
    #根据移动标志调整飞船的位置
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top>0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        self.rect.x = self.x        #虽然self.rect.x只存储self.x的整数部分，不过影响不大
        self.rect.y = self.y

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)     #surface.blit(image,(x,y),rect)  (x,y)默认(0,0)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)         #加了y轴移动的功能，这里需要同时更新y