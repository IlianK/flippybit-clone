try:
    import cairo
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

class GameRenderer:
    def __init__(self):
        pass

    def draw(self, area, cr, width, height, enemies, projectiles):
        if not HAS_CAIRO:
            return

        # Clear background
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.paint()

        # Draw enemies
        for enemy in enemies:
            if enemy.active:
                self._draw_enemy(cr, enemy)

        # Draw projectiles
        for projectile in projectiles:
            if projectile.active:
                self._draw_projectile(cr, projectile, height)

    def _draw_enemy(self, cr, enemy):
        # Enemy background
        cr.set_source_rgb(0.8, 0.2, 0.2)
        cr.rectangle(enemy.x, enemy.y, enemy.width, enemy.height)
        cr.fill()

        # Enemy text
        cr.set_source_rgb(1, 1, 1)
        cr.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(16)

        hex_str = hex(enemy.hex_value).upper()[2:].zfill(2)
        text = f"0x{hex_str}"

        # Center text
        extents = cr.text_extents(text)
        text_x = enemy.x + (enemy.width - extents.width) / 2
        text_y = enemy.y + (enemy.height + extents.height) / 2

        cr.move_to(text_x, text_y)
        cr.show_text(text)

    def _draw_projectile(self, cr, projectile, screen_height):
        # Calculate position
        current_x = projectile.start_x - projectile.width // 2
        start_y = screen_height
        target_y = projectile.target_y
        current_y = start_y - ((start_y - target_y) * projectile.progress)

        # Draw projectile
        cr.set_source_rgb(1.0, 0.2, 0.2)
        cr.rectangle(current_x, current_y - projectile.height,
                    projectile.width, projectile.height)
        cr.fill()

        # Glow effect
        cr.set_source_rgba(1.0, 0.5, 0.5, 0.3)
        cr.rectangle(current_x - 2, current_y - projectile.height - 2,
                    projectile.width + 4, projectile.height + 4)
        cr.fill()
