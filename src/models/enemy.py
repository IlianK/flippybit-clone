class Enemy:
    def __init__(self, hex_value, x, speed=1.0):
        self.hex_value = hex_value
        self.x = x
        self.y = 0
        self.speed = speed
        self.width = 80
        self.height = 40
        self.active = True
        self.marked_for_destruction = False
        self.destroy_value = None
