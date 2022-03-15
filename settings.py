class Settings():
    #创建settings类来管理游戏里所有的设置
    def __init__(self):
        #init初始化游戏的静态属性
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_limit = 3
        self.ship_speed = 1.5
        
        #子弹设置
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 6
        self.bullet_speed = 1.0

        #外星人设置
        self.fleet_drop_speed = 15
        self.alien_speed = 0.8
        self.fleet_direction = 1        #fleet_direction为1表示右移，-1表示左移。这样可以免得去写if else语句
        self.alien_points = 50

        #加快游戏节奏的速度
        self.speedup_scale = 1.3

        #外星人分数的提高速度
        self.score_scale = 1.5

    def increse_speed(self):
        #为提高游戏元素的速度，将每个速度都乘以speedup_scale的值
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)       #为了让分数为整数

    def initialize_dynamic_settings(self):
        #初始化随游戏进行而变化的属性
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.5
        self.fleet_direction = 1        #fleet_direction为1表示右移，-1表示左移。这样可以免得去写if else语句

        #记分
        self.alien_points = 50

    def set_hard_mode(self):
        self.ship_speed = 2
        self.bullet_speed = 1.5
        self.alien_speed = 2
        self.fleet_direction = 1
        self.alien_points = 200