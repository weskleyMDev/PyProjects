class Settings:
    """ A class to store settings for this game. """

    def __init__(self):
        """ Initialize the game's settings. """
        """ Screen settings. """
        self.screen_width = 1200
        self.screen_heigh = 720
        self.bg_color = (230, 230, 230)

        """ Ship settings. """
        self.ship_speed_factor = 1.5
