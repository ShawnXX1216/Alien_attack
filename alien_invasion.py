from hashlib import new
import sys
from time import sleep
from matplotlib.style import available
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button, Button_difficulty
from scoreboard import Scoreboard

#定义一个类AlienInvasion来管理游戏资源和行为
class AlienInvasion():
    def __init__(self):
        #初始化游戏，创建游戏资源
        pygame.init()       #初始化背景设置
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))       #创建一个1200*800的游戏窗口
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color       #设置背景色
        #创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        self.sb = Scoreboard(self)      #创建存储游戏统计信息的实例

        self.ship = Ship(self)      #这里的self指向的是当前AlienInvasion实例，即传递给形参ai_game
        self.bullets = pygame.sprite.Group()        #创建用于存储子弹的编组
        self.aliens = pygame.sprite.Group()         #创建用于存储外星人的编组

        self._create_fleet()

        #创建按钮
        self.play_button = Button(self, "Play")
        self.difficulty_button = Button_difficulty(self, "Hard")

    def run_game(self):
        #开始游戏的主循环
        while True:
            self._check_events()

            if self.stats.game_active:      #只有game_active为True时，游戏才会继续
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):        #辅助方法的名称用_打头
        #响应按键和鼠标事件
        for event in pygame.event.get():        #每当发生事件，就做出反应. (pygame.event.get()返回一个列表，包含上次被调用以后发生的所有事件)
            if event.type == pygame.QUIT:
                self._write_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._choose_difficulty(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self,mouse_pos):
        #在玩家单机Play时开始新游戏
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #仅当game_active为False时和单击Play按钮时重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _choose_difficulty(self,mouse_pos):
        button_clicked = self.difficulty_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.set_hard_mode()
            self._start_game()

    def _start_game(self):
        pygame.mouse.set_visible(False)         #游戏开始时隐藏光标
        self.stats.reset_stats()        #重置统计数据

        #开始游戏时更新分数图像、等级图像、剩余飞船图像
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.stats.game_active = True
        self.stats.ships_left = self.settings.ship_limit
        #清空外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        #创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self._write_score()
            sys.exit()
        elif event.key == pygame.K_RETURN:
            if not self.stats.game_active:
                self.settings.initialize_dynamic_settings()
                self._start_game()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        #创建一颗子弹并将其加入编组中
        if len(self.bullets)<self.settings.bullets_allowed:     #设置弹夹装弹量为3 （即只有在屏幕上子弹数量小于3时才能开火）
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)        #方法add()专门为pygame编写，类似于append()

    def _update_bullets(self):
        #更新子弹的位置并删除消失的子弹
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:       #如果子弹所在的rect的底部的坐标小于等于0了（即子弹消失），则将其从编组中删去 
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人。若想创建能够消灭多个外星人的高能子弹，就将第一个布尔参数设置为
        False,第二个为True，这样被击中的外星人会消失但子弹不会'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #若有外星人被击中，就加分
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        #检查外星人是否被消灭完了，如果是，就新建一群外星人
        if not self.aliens:
            self._create_fleet()
            self.settings.increse_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        #创建外星人部队
        alien = Alien(self)     #创建一个外星人
        #计算一行能容纳多少外星人 （外星人之间的间隔为其宽度的1/2）
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - alien_width        #为什么要用settings里的screen_width？因为屏幕宽度是在settings里定义的
        numbers_aliens_x = available_space_x // (2*alien_width)        #整除，丢弃余数

        #计算总共能容纳几行外星人 (初始飞船与外星人的距离设置为外星人高度的三倍)
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3*alien_height - ship_height
        number_rows = available_space_y // (2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1.5*alien_width*alien_number
        alien.y = alien_height + 1.5*alien_height*row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)      #将其添加进编队

    def _check_fleet_edges(self):
        #当外星人位于屏幕边缘时采取的行动
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #外星人群下移并改变移动方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        #检查是否有外星人位于屏幕边缘
        self._check_fleet_edges()
        #更新外星人位置
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _ship_hit(self):
        #响应飞船被外星人撞到
        if self.stats.ships_left>1:
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创造一群新的外星人
            self._create_fleet()

            #飞船数减一，并更新剩余飞船的图像
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.ship.center_ship()         #将飞船放置在屏幕底部中央
            sleep(0.5)      #暂停
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #检查是否有外星人到达了屏幕底端
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _write_score(self):
        #在退出游戏前把最高分写入文件，以便下次玩的时候读取
        filename = "Alien_attack game/data/high_score.json"
        with open(filename, 'w') as f:
            f.write(str(self.stats.high_score))

    def _update_screen(self):
        #重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #显示得分
        self.sb.show_sccore()

        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.difficulty_button.draw_button()

        #更新屏幕
        pygame.display.flip()       #刷新窗口

if __name__ == '__main__':      #当模块被直接运行时，才运行下面的代码块
    #创建游戏实例并开始游戏
    ai = AlienInvasion()
    ai.run_game()