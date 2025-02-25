
class Settings:
    """Class to manage game settings."""

    def __init__(self):
        """Initialize the game settings."""
        self.screen_width = 0
        self.screen_height = 0
        self.ship_speed = 1.5
        self.bg_color = (230,230,230)

        #Bullet Settings

        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_allowed = 3
        self.bullet_color = (60, 60, 60)

