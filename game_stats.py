class GameStats:
    #跟踪游戏的统计信息
    def __init__(self,ai_game):
        #初始化统计信息
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False         #游戏刚启动时处于非活动状态
        
        #任何情况下都不应该重置最高得分
        self.high_score = int(self.load_high_score())

    def reset_stats(self):
        #初始化游戏运行期间可能变化的统计信息
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def load_high_score(self):
        #读取最高分
        filename = "Alien_attack game/data/high_score.json"
        with open(filename) as f:
            high_score = f.read()
        return high_score