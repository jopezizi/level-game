import pygame

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Level Game")
        self.clock = pygame.time.Clock()
        
        self.load_images()
        self.run()


    def load_images(self):
        self.images={}
        bg = pygame.image.load("tausta.jpg").convert()
        bg = pygame.transform.scale(bg, (self.screen_rect.width, self.screen_rect.height))

        self.images["tausta"] = bg

    def run(self):
        runs = True
        while runs:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    runs = False
            self.screen_update()
            self.clock.tick(60)
        pygame.quit()
        exit()

    def screen_update(self):
        self.screen.blit(self.images["tausta"], (0,0))

        pygame.display.flip()

if __name__ == "__main__":
    Game()