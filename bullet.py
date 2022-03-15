import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #用来管理飞船发射出的子弹的类
    def __init__(self,ai_game):     #ai_game:当前的AilenInvasion实例
        super().__init__()        #继承父类的构造函数
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #先在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,self.settings.bullet_width, self.settings.bullet_height)  #pygame.Rect(left,top,width,height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        #向上移动子弹
        #更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        #更新rect位置
        self.rect.y = self.y
    
    def draw_bullet(self):
        #在屏幕上绘制子弹
        pygame.draw.rect(self.screen,self.settings.bullet_color,self.rect)   #使用bullet_color填充rect占据的屏幕部分