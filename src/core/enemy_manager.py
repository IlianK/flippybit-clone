import random
from gi.repository import GLib
from ..models.enemy import Enemy

class EnemyManager:
    def __init__(self, game_state, on_enemy_added=None):
        self.game_state = game_state
        self.enemies = []
        self.on_enemy_added = on_enemy_added
        self.timeout_id = None


    def generate_enemy(self, area_width):
        if not self.game_state.is_playing or self.game_state.game_over:
            return None

        min_hex, max_hex = self.game_state.get_hex_range()
        hex_value = random.randint(min_hex, max_hex)

        x = random.randint(20, area_width - 100) if area_width > 0 else 100
        speed = self.game_state.get_enemy_speed()

        enemy = Enemy(hex_value, x, speed)
        self.enemies.append(enemy)

        if self.on_enemy_added:
            self.on_enemy_added(enemy)

        return enemy


    def start_spawning(self, area_width):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)

        timeout = self.game_state.get_spawn_timeout()
        self.timeout_id = GLib.timeout_add(timeout, self._spawn_callback, area_width)


    def _spawn_callback(self, area_width):
        self.generate_enemy(area_width)
        return True  # Continue spawning


    def stop_spawning(self):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None


    def update_enemies(self, area_height):
        for enemy in self.enemies[:]:
            if enemy.active:
                enemy.y += enemy.speed
                if enemy.y > area_height:
                    return True  # Game over
        return False


    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def clear_all(self):
        self.enemies.clear()
        self.stop_spawning()


    def get_active_enemies(self):
        return [e for e in self.enemies if e.active]


    def find_lowest_matching_enemy(self, value):
        matching = [e for e in self.enemies if e.active and e.hex_value == value]
        return max(matching, key=lambda e: e.y) if matching else None
