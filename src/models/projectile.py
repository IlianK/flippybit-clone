class Projectile:
    def __init__(self, start_x, target_x, target_y, value):
        self.start_x = start_x
        self.target_x = target_x
        self.target_y = target_y
        self.value = value
        self.progress = 0.0
        self.speed = 0.08
        self.active = True
        self.width = 4
        self.height = 20
