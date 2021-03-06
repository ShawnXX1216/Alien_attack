import pygame.font

class Button:
    def __init__(self,ai_game,msg):
        #初始化按钮的属性
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        #创建按钮的Rect对象
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center

        #用_prep_msg来处理渲染
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #将msg渲染为图像，并使其在按钮上居中
        self.msg_image = self.font.render(msg, True,self.text_color,self.button_color)   
        '''用font.render方法将在msg中的文本转换为图像布尔实参可以指定开启还是关闭反锯齿功能'''

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)      #绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)       #传递一副图像以及与图像相关联的rect，从而在屏幕上绘制文本图像

class Button_difficulty():
    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        #创建按钮的Rect对象
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        #用_prep_msg来处理渲染
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #将msg渲染为图像，并使其在按钮上居中
        self.msg_image = self.font.render(msg, True,self.text_color,self.button_color)   
        '''用font.render方法将在msg中的文本转换为图像.布尔实参可以指定开启还是关闭反锯齿功能'''

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)      #绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)       #传递一副图像以及与图像相关联的rect，从而在屏幕上绘制文本图像
