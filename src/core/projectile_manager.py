from ..models.projectile import Projectile

class ProjectileManager:
    def __init__(self, on_projectile_hit=None):
        self.projectiles = []
        self.on_projectile_hit = on_projectile_hit


    def create_projectile(self, start_x, target_x, target_y, value):
        projectile = Projectile(start_x, target_x, target_y, value)
        self.projectiles.append(projectile)
        return projectile


    def update_projectiles(self):
        hits = []
        for projectile in self.projectiles[:]:
            if projectile.active:
                projectile.progress += projectile.speed
                if projectile.progress >= 1.0: # Handle Hits
                    hits.append(projectile)
                    projectile.active = False
                    self.projectiles.remove(projectile)

                    if self.on_projectile_hit:
                        self.on_projectile_hit(projectile)
        return hits


    def clear_all(self):
        self.projectiles.clear()
