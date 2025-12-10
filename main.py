import pygame, os, random

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 722))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Level Game")
        self.clock = pygame.time.Clock()
        
        self.world_x=0

        self.load_images()
        self.character()
        self.diamonds()
        self.run()


    def load_images(self):
        current_path = os.path.dirname(__file__)+"/assets/"
        self.images={}

        for image in os.listdir(current_path):
            if image.endswith((".png", ".jpg")):
                img_path = os.path.join(current_path, image)
                img_name = os.path.splitext(image)[0]
                self.images[img_name] = pygame.image.load(img_path).convert_alpha()
            if image == "tausta.jpg":
                self.images["tausta"] = pygame.transform.scale(self.images[img_name], (self.screen_rect.width, self.screen_rect.height))
    
    def character(self):
        self.char = pygame.transform.scale(self.images["character"], (self.images["character"].get_width() // 6,self.images["character"].get_height() // 6))
        self.char_rect = self.char.get_rect()
        self.char_rect.bottomleft = (170,self.screen.get_height()-60)

    def diamonds(self):


    def spawn_diamond(self):


    def run(self):
        runs = True
        while runs:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    runs = False
            #näppäimistön liike
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move(+5)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move(-5)
            #if keys[pygame.K_UP] or keys[pygame.K_w]:
            #    self.move(-3, 0)
            #if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            #    self.move(3, 0)


            self.screen_update()
            self.clock.tick(60)
        pygame.quit()
        exit()

    def move(self, x):
        if self.world_x + x > 0:
            self.world_x += 0
        else:
            self.world_x += x

    def screen_update(self):

        self.screen.blit(self.images["tausta"], (self.world_x, 0))
        self.screen.blit(self.images["tausta"], (self.world_x + self.screen.get_width(), 0))

        if self.world_x <= -self.screen.get_width():
            self.world_x = 0
        if self.world_x >= self.screen.get_width():
            self.world_x = 0

        self.ground_piece = pygame.transform.scale(self.images["ground"], (self.images["ground"].get_width() // 4,self.images["ground"].get_height() // 4))
        ground_x = self.world_x
        while ground_x <= self.screen.get_width():
            self.screen.blit(self.ground_piece, (ground_x, 540))
            ground_x += self.ground_piece.get_width()

        self.screen.blit(self.char, (self.char_rect.x, self.char_rect.y))

        pygame.display.flip()


class Diamonds:

class Traps:
    pass

if __name__ == "__main__":
    Game()