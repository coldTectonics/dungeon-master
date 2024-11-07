import pygame, sys
from pygame.locals import *
import random, time
import numpy
from entities import Hero, EnemyMelee, EnemyArcher

class States:
    def __init__ (self):
        self.menu_screen = 1
        self.gameplay_screen = 0
        self.help_screen = 0
        self.pause_screen = 0

class GlobalSettings:

    def __init__ (self):
        self.FPS = 24
        self.FramePerSec = pygame.time.Clock()

        # Настройки экрана
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 768
        self.displaysurf = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 128, 0)
        self.RED = (128, 0, 0)
        self.ORANGE = (255, 128, 0)
        self.BLACK = (0, 0, 0)
        self.L_GREEN = (0, 255, 0)
        self.L_BLUE = (0, 0, 255)
        self.CYAN = (0, 255, 255)
        self.SHADOW = (64, 64, 64)    

        #расчёт тайлов
        self.tilesX = int(self.SCREEN_WIDTH / 16)
        self.tilesY = int(self.SCREEN_HEIGHT / 16)
        self.brick = pygame.image.load("gfx/brick.png").convert()
        self.font = pygame.font.Font("font/minecraft.ttf", 16)
        self.shadow_img = pygame.image.load("gfx/shadow.png").convert_alpha()

    def quitGame (self):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            print(f"Key {pygame.key.name(event.key)} pressed")

            if event.key == pygame.K_q:
                if event.mod & pygame.KMOD_CTRL:      
                    pygame.quit()
                    sys.exit()

        elif event.type == pygame.KEYUP:
            print(f"Key {pygame.key.name(event.key)} released")


    def tileBackground(self, texture) -> None:
    
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                self.displaysurf.blit(texture, (x * 16, y * 16))

class StartMenu (GlobalSettings):

    def __init__ (self):
        super().__init__ ()
        self.btn_count = 0
        self.font_big = pygame.font.Font("font/minecraft.ttf", 64)
        self.font_bigger = pygame.font.Font("font/minecraft.ttf", 128)

        self.btn1 = Button ('Start', self, (329,448), 0)
        self.btn2 = Button ('Help', self, (329,576), 1)
        self.ok_btn = Button ('OK', self, (329,576), 0)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.btn1)
        self.all_sprites.add(self.btn2)

    def scroll (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:

                if self.btn_count == 0:
                    self.btn_count = 1
                else:
                    self.btn_count = 0

            if event.key == pygame.K_DOWN:

                if self.btn_count == 0:
                    self.btn_count = 1
                else:
                    self.btn_count = 0

            if event.key == pygame.K_RETURN:

                if self.btn_count == 0:
                    states.menu_screen = 0
                    states.gameplay_screen = 1
                else:
                    states.menu_screen = 0
                    states.help_screen = 1

    def drawLogo (self):
        self.displaysurf.blit (self.font_bigger.render ('DUNGEON', False, self.BLACK), (329, 48))
        self.displaysurf.blit (self.font_bigger.render ('DUNGEON', False, self.BLACK), (329, 40))
        self.displaysurf.blit (self.font_bigger.render ('DUNGEON', False, self.WHITE), (329, 32))

        self.displaysurf.blit (self.font_bigger.render ('SANDBOX', False, self.BLACK), (329, 256))
        self.displaysurf.blit (self.font_bigger.render ('SANDBOX', False, self.BLACK), (329, 248))
        self.displaysurf.blit (self.font_bigger.render ('SANDBOX', False, self.WHITE), (329, 240))

        for entity in self.all_sprites:
            entity.update ()
            self.displaysurf.blit(entity.surf, entity.origin)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, menu, origin, number):
        super().__init__ () 
        self.text = text
        self.origin = origin
        self.number = number
        self.surf = pygame.Surface((48*len (text), 64))
        self.surf.fill(menu.SHADOW)
        self.surf.blit(menu.font_big.render (text, False, menu.BLACK), (0,0))

    def update (self):
        if menu.btn_count == self.number:
            self.surf.fill(menu.WHITE)
        else:
            self.surf.fill(menu.SHADOW)

        self.surf.blit(menu.font_big.render (self.text, False, menu.BLACK), (0,0))

class PauseMenu (GlobalSettings):
    pass

class Gameplay (GlobalSettings):

    def moveCharacter (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                hero.y -= hero.speed

            if event.key == pygame.K_DOWN:
                hero.y += hero.speed

            if event.key == pygame.K_LEFT:
                hero.x -= hero.speed

            if event.key == pygame.K_RIGHT:
                hero.x += hero.speed

            if event.key == pygame.K_ESCAPE:
                states.gameplay_screen = 0
                states.pause_screen = 1

    
    def renderHero(self, color):
        pygame.draw.rect(self.displaysurf, self.SHADOW, pygame.Rect(hero.x - 4, hero.y - 4, 32, 32))
        pygame.draw.rect(self.displaysurf, color, pygame.Rect(hero.x, hero.y, 32, 32))

    def renderEnemy(self, color, name):
        pygame.draw.rect(self.displaysurf, self.SHADOW, pygame.Rect(name.x - 4, name.y - 4, 32, 32))
        pygame.draw.rect(self.displaysurf, color, pygame.Rect(name.x, name.y, 32, 32))

    def renderBullet(self, color, name):
        pygame.draw.rect(self.displaysurf, color, pygame.Rect(name.x, name.y, 8, 8))

    def renderStats (self, hp, power):
        pygame.draw.rect(self.displaysurf, self.L_GREEN, pygame.Rect(16, 16, hp, 16))
        pygame.draw.rect(self.displaysurf, self.L_BLUE, pygame.Rect(16, 32, power * 5, 16))
        self.displaysurf.blit (self.font.render (str(hp) + ' HP', False, self.GREEN), (16, 16))
        self.displaysurf.blit (self.font.render (str(power) + ' PWR', False, self.CYAN), (16, 32))

    def switchInfo (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.info_screen = 1
                self.main_screen = 0
                self.help_screen = 0
        
            if event.key == pygame.K_g:
                self.info_screen = 0
                self.main_screen = 1
                self.help_screen = 0

            if event.key == pygame.K_h:
                self.info_screen = 0
                self.main_screen = 0
                self.help_screen = 1
    


if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Dungeon Sandbox")

    # Создание главного героя
    hero = Hero(hp=100, power=20, x=648, y=360, speed=32, protect=5)

    # Создание врага
    enemy_melee_1 = EnemyMelee(hp=100, power=20, x=256, y=256, speed=4, protect=5)
    enemy_melee_2 = EnemyMelee(hp=100, power=20, x=512, y=512, speed=8, protect=5)
    archer_1 = EnemyArcher (hp=100, power=20, x=400, y=400, speed=8, protect=5)
    archer_2 = EnemyArcher (hp=100, power=20, x=800, y=400, speed=8, protect=5)

    dungeon = Gameplay ()
    menu = StartMenu ()
    states = States ()
    pygame.display.set_icon(pygame.transform.scale (pygame.image.load('gfx/brick.png'), (32,32)))

    while True:

        while states.menu_screen:
            dungeon.tileBackground (dungeon.brick)
            for event in pygame.event.get():
                menu.quitGame ()
                menu.scroll ()
            menu.drawLogo ()
            pygame.display.flip()
            dungeon.FramePerSec.tick(dungeon.FPS)

        while states.gameplay_screen:

            dungeon.tileBackground (dungeon.brick)
            #dungeon.displaysurf.fill(dungeon.WHITE)
            for event in pygame.event.get():
                    dungeon.moveCharacter ()
                    dungeon.quitGame ()

            enemy_melee_1.move_towards_player (hero)
            enemy_melee_2.move_towards_player (hero)
            archer_1.update ()
            archer_1.bullet.update (dungeon, hero)
            archer_2.update ()
            archer_2.bullet.update (dungeon, hero)

            dungeon.renderHero (dungeon.GREEN)
            dungeon.renderEnemy (dungeon.RED, enemy_melee_1)
            dungeon.renderEnemy (dungeon.RED, enemy_melee_2)
            dungeon.renderEnemy (dungeon.ORANGE, archer_1)
            dungeon.renderEnemy (dungeon.ORANGE, archer_2)
            dungeon.renderBullet (dungeon.WHITE, archer_1.bullet)
            dungeon.renderBullet (dungeon.WHITE, archer_2.bullet)
            dungeon.renderStats (hero.hp, hero.power)
            pygame.display.flip()
            dungeon.FramePerSec.tick(dungeon.FPS)

        while states.help_screen:
            menu.tileBackground (menu.brick)
            menu.displaysurf.blit (menu.font_big.render ('бубубубу', False, menu.WHITE), (329, 240))
            menu.btn_count = 0
            menu.ok_btn.update()
            menu.displaysurf.blit(menu.ok_btn.surf, menu.ok_btn.origin)
            for event in pygame.event.get():
                menu.quitGame ()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        states.menu_screen = 1
                        states.help_screen = 0

            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)

        if states.pause_screen:
            dungeon.tileBackground (dungeon.shadow_img) #это сделать получше
            dungeon.tileBackground (dungeon.shadow_img)

        while states.pause_screen:
            dungeon.displaysurf.blit (menu.font_big.render ('бубубубу', False, menu.WHITE), (329, 240))
            
            for event in pygame.event.get():
                dungeon.quitGame ()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print ('тут')
                        states.gameplay_screen = 1
                        states.pause_screen = 0

            pygame.display.flip()
            dungeon.FramePerSec.tick(menu.FPS)
