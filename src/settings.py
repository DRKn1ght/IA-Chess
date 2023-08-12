class Settings:
    """ A class to manage the game settings """

    def __init__(self):
        """ Create a new settings instance """
        self.screen_width = 600
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)

        self.dark_color = (145,68,0)
        self.light_color = (255,255,255)

        self.square_size = self.screen_width // 8

        self.movement_color = (255,0,0)
        self.active_color = (0,255,0)
        self.text_color = (255,255,255)

        self.FPS = 500

        self.StockFish_Path = "D:\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2"
