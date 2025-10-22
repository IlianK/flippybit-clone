class GameConfig:
    # Difficulty settings
    INITIAL_SPAWN_TIME = 3000  # 3 seconds
    MIN_SPAWN_TIME = 1500      # 1.5 seconds
    SPAWN_TIME_DECREASE = 100  # ms per point

    INITIAL_SPEED = 0.5
    SPEED_INCREASE = 0.05       # per point

    # Hex value ranges by score
    HEX_RANGES = [
        (1, 15),    # Score 0-4: 0x01-0x0F
        (1, 63),    # Score 5-9: 0x01-0x3F
        (1, 127),   # Score 10-14: 0x01-0x7F
        (1, 255)    # Score 15+: 0x01-0xFF
    ]

    @classmethod
    def get_hex_range(cls, score):
        if score < 5:
            return cls.HEX_RANGES[0]
        elif score < 10:
            return cls.HEX_RANGES[1]
        elif score < 15:
            return cls.HEX_RANGES[2]
        else:
            return cls.HEX_RANGES[3]
