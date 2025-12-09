import pygame

class Game:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.run()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Level Game")
        self.clock = pygame.time.Clock()
        
        self.loop()

    def load_images(self):
        self.images=[]
        self.filenames =[
            "hahmo",
        ]

        for filename in self.filenames:
            self.images.append(pygame.image.load(nimi+".png"))

    def run(self):
        