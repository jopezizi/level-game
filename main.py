import pygame, os, random

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 722))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Level Game")
        self.clock = pygame.time.Clock()
        
        self.world_x=0
        self.world_offset = 0
        self.background_x = 0 
        self.last_monster_spawn = 0
        self.monsters = []
        self.load_images()
        self.character()
        self.set_timer()
        self.spawn_diamond()
        # self.spawn_bricks()
        self.spawn_monsters()
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
        self.char_rect.bottomleft = (self.screen.get_width()//2-self.char.get_width()//2,self.screen.get_height()-60)

    def spawn_diamond(self):
        self.diamonds = []
        amount = 50
        x = 500
        for i in range(amount):
            diamond_gap = random.randint(400,3500)

            x += diamond_gap
            y = 590
            self.diamonds.append(
                Diamonds(self.images["diamond"],x,y)
            )
    
    def spawn_monsters(self):
        amount = 25
        for i in range(amount):
            screen_x = random.randint(0, self.screen.get_width()+4000)

            x = screen_x - self.world_offset
            y = random.randint(-700, -300)

            self.monsters.append(
                Monsters(self.images["monster"],x,y)
            )



    def set_timer(self):
        self.timer = Timer()

    # def spawn_bricks(self):
    #     self.bricks = []
    #     amount = 50
    #     x = 500
    #     for i in range(amount):
    #         brick_gap = random.randint(400,2000)

    #         x += brick_gap
    #         y = 590
    #         self.bricks.append(
    #             Bricks(self.images["brick"],x,y)
    #         )



    def run(self):
        runs = True
        while runs:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.USEREVENT:
                    self.timer.countdown -= 1
                    self.timer.text = str(self.timer.countdown).rjust(3) if self.timer.countdown > 0 else '0'
                if tapahtuma.type == pygame.QUIT:
                    runs = False
            #näppäimistön liike
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move(+6)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move(-6)
            #if keys[pygame.K_UP] or keys[pygame.K_w]:
            #    self.move(-3, 0)
            #if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            #    self.move(3, 0)

            
            self.screen_update()
            self.clock.tick(60)
        pygame.quit()
        exit()

    def move(self, x):
        if x < 0:
            self.world_offset += x
            self.background_x += x
        if self.world_offset + x <= 0:
            self.world_offset += x
            self.background_x += x

        char_loc_x = -self.world_offset
        if abs(char_loc_x - self.last_monster_spawn) > 1000:
            self.spawn_monsters()
            self.last_monster_spawn = char_loc_x

    def screen_update(self):

        self.screen.blit(self.images["tausta"], (self.background_x, 0))
        self.screen.blit(self.images["tausta"], (self.background_x + self.screen.get_width(), 0))

 

        if self.background_x <= -self.screen.get_width():
            self.background_x = 0
        if self.background_x >= self.screen.get_width():
            self.background_x = 0


        self.ground_piece = pygame.transform.scale(self.images["ground"], (self.images["ground"].get_width() // 4,self.images["ground"].get_height() // 4))
        ground_x = self.world_offset
        while ground_x <= self.screen.get_width():
            self.screen.blit(self.ground_piece, (ground_x, 540))
            ground_x += self.ground_piece.get_width()

        self.screen.blit(self.char, (self.char_rect.x, self.char_rect.y))

        self.screen.blit(self.timer.font.render(self.timer.text, True, (255,255,255)),(1170,40))

        # for brick in self.bricks:
        #     brick.update(self.world_offset)
        #     brick.screen_update(self.screen)

        for diamond in self.diamonds:
            diamond.update(self.world_offset)
            diamond.screen_update(self.screen)

        for monster in self.monsters:
            monster.update(self.world_offset)
            monster.screen_update(self.screen)

        pygame.display.flip()


class Diamonds:
    def __init__(self, image, world_x, y):
        self.image = pygame.transform.scale(image,(60,60))
        self.world_x = world_x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.y = y

    def update(self, world_x):
        self.rect.x = self.world_x + world_x
    
    def screen_update(self, screen):
        screen.blit(self.image, self.rect)

class Monsters:
    def __init__(self, image, world_x, y):
        self.image = pygame.transform.scale(image,(image.get_width() // 6, image.get_height() // 6))
        self.world_x = world_x
        self.y = y
        self.fallspeed = 0
        self.gravity = 0.15

        self.falling = False
        self.rect = self.image.get_rect()
        self.rect.y = y

    def update(self, world_offset):

        screen_x = self.world_x + world_offset
        self.rect.x = screen_x

        if screen_x < 1280 + 200 and not self.falling:
            self.falling = True

        if not self.falling:
            return
        
        self.fallspeed += self.gravity
        self.rect.y += self.fallspeed
        ground_y = 480

    
    def screen_update(self, screen):
        screen.blit(self.image, self.rect)

class Timer:
    def __init__(self):
        self.countdown, self.text = 60 , '60'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.font = pygame.font.SysFont('Arial', 50)

# class Bricks:
        def __init__(self, image, world_x, y):
            self.image = pygame.transform.scale(image,(70,70))
            self.world_x = world_x
            self.y = y

            self.rect = self.image.get_rect()
            self.rect.y = y
        
        def update(self,world_x):
            self.rect.x = self.world_x + world_x

        def screen_update(self, screen):
            screen.blit(self.image, self.rect)
if __name__ == "__main__":
    Game()