from ..models.game_config import GameConfig

class GameState:
    def __init__(self):
        self.score = 0
        self.is_playing = False
        self.game_over = False


    def reset(self):
        self.score = 0
        self.is_playing = True
        self.game_over = False


    def increment_score(self):
        self.score += 1


    def get_spawn_timeout(self):
        return max(
            GameConfig.MIN_SPAWN_TIME,
            GameConfig.INITIAL_SPAWN_TIME - (self.score * GameConfig.SPAWN_TIME_DECREASE)
        )


    def get_enemy_speed(self):
        return GameConfig.INITIAL_SPEED + (self.score * GameConfig.SPEED_INCREASE)


    def get_hex_range(self):
        return GameConfig.get_hex_range(self.score)
