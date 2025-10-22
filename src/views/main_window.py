from gi.repository import Adw, Gtk, GLib
from ..ui import GameArea  # Import from ui module
from ..core.game_state import GameState
from ..core.enemy_manager import EnemyManager
from ..core.projectile_manager import ProjectileManager
from ..core.input_handler import InputHandler
from ..views.bit_display import BitDisplay
from ..views.game_renderer import GameRenderer

@Gtk.Template(resource_path='/com/example/flippybit/ui/main_window.ui')
class FlippybitWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'FlippybitWindow'

    score_label = Gtk.Template.Child()
    main_content = Gtk.Template.Child()  # Add this template child

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize components
        self.game_state = GameState()
        self.game_renderer = GameRenderer()

        # Create game area
        self.game_area = GameArea()
        self.main_content.append(self.game_area)  # Use the template child

        # Rest of the code remains the same...
        # Initialize managers
        self.enemy_manager = EnemyManager(
            self.game_state,
            on_enemy_added=self._on_enemy_added
        )

        self.projectile_manager = ProjectileManager(
            on_projectile_hit=self._on_projectile_hit
        )

        # Initialize bit display
        self.bit_display = BitDisplay(
            self.game_area.bit_container,
            on_bit_clicked=self._on_bit_clicked
        )

        # Initialize input handler
        self.input_handler = InputHandler(on_bit_flip=self._on_bit_flipped)
        self.add_controller(self.input_handler.controller)

        # Connect signals
        self.game_area.start_button.connect("clicked", self._on_start_game)
        self.game_area.game_area.set_draw_func(self._draw_game_area)

        # Animation
        self.animation_id = None


    def _on_start_game(self, button):
        if self.game_state.is_playing and not self.game_state.game_over:
            return

        self.game_state.reset()
        self.score_label.set_label("0")
        self.game_area.start_button.set_label("Restart Game")
        self.game_area.status_label.set_label("Game running! Use 1-8 keys or click bits!")

        self.bit_display.reset()
        self._update_live_hex_display()

        self.enemy_manager.clear_all()
        self.projectile_manager.clear_all()

        area_width = self.game_area.game_area.get_allocation().width
        self.enemy_manager.start_spawning(area_width)
        self._start_animation()

    def _on_bit_clicked(self, button, bit_index):
        if not self.game_state.is_playing or self.game_state.game_over:
            return
        self.bit_display.flip_bit(bit_index)
        self._update_live_hex_display()
        self._check_auto_fire()

    def _on_bit_flipped(self, bit_index):
        if not self.game_state.is_playing or self.game_state.game_over:
            return
        self.bit_display.flip_bit(bit_index)
        self._update_live_hex_display()
        self._check_auto_fire()

    def _update_live_hex_display(self):
        value = self.bit_display.get_binary_value()
        hex_value = hex(value).upper()[2:].zfill(2)
        self.game_area.live_hex_label.set_label(f"0x{hex_value}")

    def _check_auto_fire(self):
        if not self.game_state.is_playing or self.game_state.game_over:
            return

        current_value = self.bit_display.get_binary_value()
        if current_value == 0:
            return

        target_enemy = self.enemy_manager.find_lowest_matching_enemy(current_value)
        if target_enemy:
            start_x = target_enemy.x + target_enemy.width // 2
            enemy_center_x = target_enemy.x + target_enemy.width // 2
            enemy_center_y = target_enemy.y + target_enemy.height // 2

            self.projectile_manager.create_projectile(
                start_x, enemy_center_x, enemy_center_y, current_value
            )

            target_enemy.marked_for_destruction = True
            target_enemy.destroy_value = current_value

            hex_str = hex(current_value).upper()[2:].zfill(2)
            self.game_area.status_label.set_label(f"Auto-firing 0x{hex_str} at enemy!")

            GLib.timeout_add(100, self._reset_bits_delayed)

    def _reset_bits_delayed(self):
        self.bit_display.reset()
        self._update_live_hex_display()
        return False

    def _on_enemy_added(self, enemy):
        # Could add visual effects when enemy spawns
        pass

    def _on_projectile_hit(self, projectile):
        for enemy in self.enemy_manager.get_active_enemies():
            if hasattr(enemy, 'marked_for_destruction') and enemy.marked_for_destruction:
                self.enemy_manager.remove_enemy(enemy)
                self.game_state.increment_score()
                self.score_label.set_label(str(self.game_state.score))

                # Visual feedback
                original_classes = self.game_area.live_hex_label.get_css_classes()
                self.game_area.live_hex_label.set_css_classes(original_classes + ["success"])
                GLib.timeout_add(300, lambda: self.game_area.live_hex_label.set_css_classes(original_classes))

                self.game_area.status_label.set_label("Hit! Enemy destroyed!")
                break

    def _draw_game_area(self, area, cr, width, height):
        self.game_renderer.draw(
            area, cr, width, height,
            self.enemy_manager.enemies,
            self.projectile_manager.projectiles
        )

    def _start_animation(self):
        if self.animation_id:
            GLib.source_remove(self.animation_id)
        self.animation_id = GLib.timeout_add(16, self._update_animation)

    def _update_animation(self):
        if not self.game_state.is_playing:
            return False

        area_height = self.game_area.game_area.get_allocation().height

        # Update enemies
        game_over = self.enemy_manager.update_enemies(area_height)
        if game_over:
            self._stop_game(game_over=True)
            return False

        # Update projectiles
        self.projectile_manager.update_projectiles()

        # Redraw
        self.game_area.game_area.queue_draw()
        return True

    def _stop_game(self, game_over=False):
        self.game_state.is_playing = False
        self.game_state.game_over = game_over

        self.enemy_manager.stop_spawning()
        if self.animation_id:
            GLib.source_remove(self.animation_id)
            self.animation_id = None

        if game_over:
            self.game_area.status_label.set_label("Game Over! An enemy reached the bottom!")
        else:
            self.game_area.status_label.set_label("Game stopped. Click Start to play again!")
