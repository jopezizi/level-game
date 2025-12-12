import pygame, os, random, math

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 722))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Level Game")
        self.clock = pygame.time.Clock()
        
        # alustetaan tarvittavat muuttujat
        self.world_x=0
        self.world_offset = 0
        self.bg_offset = 0 
        self.last_monster_spawn = 0
        self.monsters = []

        
        self.load_images()
        self.character()
        self.set_timer()
        self.set_counter()
        self.set_lives()
        self.spawn_coin()
        self.spawn_monsters()
        self.run()


    def load_images(self): #lataa kaikki kuvat kansiosta
        current_path = os.path.dirname(__file__)+"/assets/"
        self.images={}

        for image in os.listdir(current_path):
            if image.endswith((".png", ".jpg")):
                img_path = os.path.join(current_path, image)
                img_name = os.path.splitext(image)[0]
                self.images[img_name] = pygame.image.load(img_path).convert_alpha()
    
    def character(self): # robo
        self.char = pygame.transform.scale(self.images["robo"], (self.images["robo"].get_width()*1.3,self.images["robo"].get_height()*1.3))
        self.char_rect = self.char.get_rect()
        self.char_rect.bottomleft = (self.screen.get_width()//2-self.char.get_width()//2,self.screen.get_height()-60)

    def spawn_coin(self): # metodi, joka synnyttää kolikot satunnaisen etäisyyden päähän
        self.coins = []
        amount = 50
        x = 500
        for i in range(amount):
            coin_gap = random.randint(400,3100)

            x += coin_gap
            y = 590
            self.coins.append(
                Coins(self.images["kolikko"],x,y)
            )
    
    def spawn_monsters(self): # metodi, joka synnyttää hirviöt satunnaisen etäsidyyden päähän.
        amount = 25
        for i in range(amount):
            screen_x = random.randint(0, self.screen.get_width()+4500)

            x = screen_x - self.world_offset
            y = random.randint(-1000, -300)

            self.monsters.append(
                Monsters(self.images["hirvio"],x,y)
            )



    def set_timer(self): # luo ajastinolion
        self.timer = Timer()

    def set_counter(self): # luo kolikkolaskuriolion
        self.counter = Counter()

    def set_lives(self): # luo elämälaskuriolion
        self.lives = Lives()


    def run(self): # suoritussilmukka
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
                self.move(+12)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move(-12)

            
            self.screen_update()
            self.clock.tick(60)
        pygame.quit()
        exit()

    def move(self, x): # metodi, joka liikuttaa maailmaa, hahmo pysyy paikallaan, saadaan illuusio jatkuvuudesta
        
        if x < 0 or self.world_offset + x <= 0:
            self.world_offset += x
            self.bg_offset += x *1.5

        char_loc_x = -self.world_offset
        if abs(char_loc_x - self.last_monster_spawn) > 1000:
            self.spawn_monsters()
            self.last_monster_spawn = char_loc_x

    def screen_update(self): # näytön päivitysmetodi
        
        # luodaan tausta
        bg = pygame.Surface(self.screen.get_size())
        bg.fill((100, 0, 100))
        self.screen.blit(bg, (0, 0))

        # luodaan "maa"
        pygame.draw.rect(self.screen, (140,30,255),pygame.Rect(0,660,self.screen.get_width(),70))

        # ohjeteksti
        self.screen.blit(pygame.font.SysFont('Arial', 20).render("Kerää 7 kolikkoa ennen kuin aika loppuu! Väistele hirviöitä, sinulla on kolme elämää.", True, (255,255,255)),(300,100))

        # hahmo
        self.screen.blit(self.char, (self.char_rect.x, self.char_rect.y))

        # ajastin
        self.screen.blit(self.timer.font.render(self.timer.text, True, (255,255,255)),(1170,40))

        # kolikkolaskuri ...
        countertext = self.counter.font.render(self.counter.textstr, True, (255,255,255))
        self.screen.blit(countertext, (100,40))
        # ... jonka viereen kolikon kuva selketykseksi
        text_h = countertext.get_height()
        coin = pygame.transform.scale(self.images["kolikko"], (text_h, text_h))
        self.screen.blit(coin, (100 - text_h - 5, 40))

        # elämälaskuri
        self.screen.blit(self.lives.font.render(self.lives.textstr, True, (255,255,255)),(500,40))

        # kolikon sijainnin päivitys, liikkuu taustan mukana samanaikaisesti
        for coin in self.coins:
            coin.update(self.world_offset)
            coin.screen_update(self.screen)

        # jos hahmo osuu kolikkoon, poistetaan se ja lisätään laskuriin +1
        for coin in self.coins:
            if self.char_rect.x <= coin.rect.x + coin.image.get_width() and self.char_rect.x + self.char.get_width() >= coin.rect.x+20:
                self.coins.remove(coin)
                self.counter.text += 1
                self.counter.textstr = f"{str(self.counter.text)}/7".rjust(5)
        
        # hirviön sijainnin päivitys, liikkuu tasutan mukana samanaikaisesti
        for monster in self.monsters:
            monster.update(self.world_offset)
            monster.screen_update(self.screen)

        # jos hahmo osuu hirviöön, poistetaan se ja vähennetään yksi elämä
        for monster in self.monsters:
            if self.char_rect.colliderect(monster.rect):
                self.monsters.remove(monster)
                self.lives.text -= 1
                self.lives.textstr = f"Elämät: {str(self.lives.text)}/3".rjust(3)

        # jos pelaaja saa 10 kolikkoa, voitit pelin- näyttö
        if self.counter.text == 7:
            fade = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            fade.fill((0,0,0))
            fade.set_alpha(240)
            self.screen.blit(fade, (0,0))
            font = pygame.font.SysFont('Arial', 100)
            text_surf = font.render('VOITIT PELIN', True, (0,128,0))
            text_rect = text_surf.get_rect(center = (self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(text_surf, text_rect)

        # jos aika loppuu, hävisit pelin- näyttö
        if self.timer.countdown <= 0:
            fade = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            fade.fill((0,0,0))
            fade.set_alpha(240)
            self.screen.blit(fade, (0,0))
            font = pygame.font.SysFont('Arial', 100)
            text_surf = font.render('HÄVISIT PELIN', True, (128,0,0))
            text_rect = text_surf.get_rect(center = (self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(text_surf, text_rect)

        # jos elämät loppuu, myös hävisit pelin- näyttö
        if self.lives.text <= 0:
            self.lives.textstr = "0/3".rjust(3)
            fade = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            fade.fill((0,0,0))
            fade.set_alpha(240)
            self.screen.blit(fade, (0,0))
            font = pygame.font.SysFont('Arial', 100)
            text_surf = font.render('HÄVISIT PELIN', True, (128,0,0))
            text_rect = text_surf.get_rect(center = (self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(text_surf, text_rect)

        pygame.display.flip()

# kolikko-olio
class Coins:
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

#hirviö-olio
class Monsters:
    def __init__(self, image, world_x, y):
        self.image = pygame.transform.scale(image,(image.get_width()*2, image.get_height()*2))
        self.world_x = world_x
        self.y = y
        self.fallspeed = 4
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

    
    def screen_update(self, screen):
        screen.blit(self.image, self.rect)

# ajastinolio
class Timer:
    def __init__(self):
        self.countdown, self.text = 45 , '45'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.font = pygame.font.SysFont('Arial', 50)

# kolikkolaskuriolio
class Counter:
    def __init__(self):
        self.text = 0
        self.textstr = f"{str(self.text)}/7".rjust(5)
        self.font = pygame.font.SysFont('Arial', 50)

# elämälaskuriolio
class Lives:
    def __init__(self):
        self.text = 3
        self.textstr = f"Elämät: {str(self.text)}/3".rjust(3)
        self.font = pygame.font.SysFont('Arial', 50)


if __name__ == "__main__":
    Game()