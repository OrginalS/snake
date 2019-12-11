class Settings:
    """Game settings"""

    def __init__(self):
        """Initialize game settings"""
        self.screen_size = (600, 600)
        self.bg_color = (200, 200, 200)
        self.block = 20
        self.ai_enabled = False
        self.lines_enabled = False
        self.sound_enabled = True
        self.dark_mode_enabled = False
