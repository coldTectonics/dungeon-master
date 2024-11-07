import pygame, sys
from pygame.locals import *
import random
from entities import Hero, EnemyMelee, EnemyArcher, HealthPack, EnergyPack, Key, Lock, Amulet, Gem, Cig, Pistol
from graphics import Landscape

class States: #состояния игры
    def __init__ (self):
        self.menu_screen = 1
        self.gameplay_screen = 0
        self.help_screen = 0
        self.pause_screen = 0
        self.console_screen = 0
        self.inventory_screen = 0
        self.game_over_screen = 0
        self.times_pause = 0
        self.restart = 0

class PauseGfx: #тут хранится игровой экран при паузе
    def __init__ (self, x):
        self.x = x

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
        self.font_medium = pygame.font.Font("font/minecraft.ttf", 32)
        self.font_big = pygame.font.Font("font/minecraft.ttf", 64)
        self.font_bigger = pygame.font.Font("font/minecraft.ttf", 128)
        self.shadow_img = pygame.image.load("gfx/shadow.png").convert_alpha()

        #звуки
        self.scroll_sound = pygame.mixer.Sound("sound/menusnd01.wav")
        self.select_sound = pygame.mixer.Sound("sound/menusnd02.wav")
        self.die_sound = pygame.mixer.Sound("sound/boom-shipdie.wav")
        self.shoot_sound = pygame.mixer.Sound("sound/spathi-bullet.wav")
        self.impact_sound = pygame.mixer.Sound("sound/boom-tiny.wav")
        self.player_die_sound = pygame.mixer.Sound("sound/druuge-furnace.wav")
        self.footsteps_sound = pygame.mixer.Sound("sound/minecraft-footsteps.mp3")

    def quitGame (self):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #print(f"Key {pygame.key.name(event.key)} pressed")

            if event.key == pygame.K_q:
                if event.mod & pygame.KMOD_CTRL:      
                    pygame.quit()
                    sys.exit()

        elif event.type == pygame.KEYUP:
            #print(f"Key {pygame.key.name(event.key)} released")
            pass


    def tileBackground(self, texture) -> None:
        t_s = pygame.transform.scale (texture, (32,32))
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                self.displaysurf.blit(t_s, (x * 32, y * 32))

class Menu (GlobalSettings):

    def __init__ (self):
        super().__init__ ()
        self.btn_count = 0
        self.btn_max = 0
        self.all_buttons = pygame.sprite.Group()

    def scroll (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.scroll_sound.play()
                if self.btn_count == 0:
                    self.btn_count = self.btn_max
                else:
                    self.btn_count -= 1

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.scroll_sound.play()
                if self.btn_count == self.btn_max:
                    self.btn_count = 0
                else:
                    self.btn_count += 1

    def pressReturn (self):
        pass

    def drawButtons (self, x):
        for entity in self.all_buttons:
            entity.update (x)
            self.displaysurf.blit(entity.surf, entity.origin)

class StartMenu (Menu): #стартовый экран

    def __init__ (self):
        super().__init__ ()
        self.btn_max = 1 
        self.btn1 = Button ('Start', (329,448), 0)
        self.btn2 = Button ('Help', (329,576), 1)
        self.ok_btn = Button ('OK', (329,576), 0)
        self.all_buttons.add(self.btn1)
        self.all_buttons.add(self.btn2)

    def pressReturn (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.select_sound.play()
                if self.btn_count == 0:
                    states.menu_screen = 0
                    states.gameplay_screen = 1
                    states.restart = 1

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

class Button(pygame.sprite.Sprite):
    def __init__(self, text, origin, number):
        super().__init__()
        self.SHADOW = (64, 64, 64)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.font_big = pygame.font.Font("font/minecraft.ttf", 64)
        self.text = text
        self.origin = origin
        self.number = number
        self.surf = pygame.Surface((48*len (self.text), 64))
        self.surf.fill(self.SHADOW)
        self.surf.blit(self.font_big.render (self.text, False, self.BLACK), (0,0))

    def update (self, btn_count):
        if btn_count == self.number:
            self.surf.fill(self.WHITE)
        else:
            self.surf.fill(self.SHADOW)

        self.surf.blit(self.font_big.render (self.text, False, self.BLACK), (0,0))

class PauseMenu (Menu): #выводит меню паузы

    def __init__ (self):
        super().__init__ ()
        self.btn_max = 2 
        self.btn1 = Button ('Resume',  (329,320), 0)
        self.btn2 = Button ('Inventory', (329,448), 1)
        self.btn3 = Button ('Main menu', (329,576), 2)
        self.all_buttons = pygame.sprite.Group()
        self.all_buttons.add(self.btn1)
        self.all_buttons.add(self.btn2)
        self.all_buttons.add(self.btn3)

    def pressReturn (self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.select_sound.play()
                match self.btn_count:
                    case 0:
                        states.pause_screen = 0
                        states.gameplay_screen = 1
                    case 1:
                        states.pause_screen = 0
                        states.inventory_screen = 1
                    case 2:
                        states.pause_screen = 0
                        states.menu_screen = 1
            elif event.key == pygame.K_ESCAPE:
                states.pause_screen = 0
                states.gameplay_screen = 1
                

class Gameplay (GlobalSettings):
    def __init__(self):
        super().__init__ ()
        self.shadowsurf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.shadowsurf.set_colorkey ((255, 255, 255))
        self.shadowsurf.set_alpha (255)
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 128, 0)
        self.RED = (128, 0, 0)
        self.ORANGE = (255, 128, 0)

        self.melee_img = pygame.image.load("gfx/devil.png").convert_alpha ()
        self.archer_img = pygame.image.load("gfx/skull.png").convert_alpha ()
        self.hero_img = pygame.image.load("gfx/cool.png").convert_alpha ()
        self.sceptical_img = pygame.image.load("gfx/sceptical.png").convert_alpha ()
        self.crying_img = pygame.image.load("gfx/crying.png").convert_alpha ()
        self.health_img = pygame.image.load("gfx/heart.png").convert_alpha ()
        self.energy_img = pygame.image.load("gfx/energy.png").convert_alpha ()
        self.amulet_img = pygame.image.load("gfx/amulet.png").convert_alpha ()
        self.coffin_img = pygame.image.load("gfx/coffin.png").convert_alpha ()
        self.key_img = pygame.image.load("gfx/key.png").convert_alpha ()
        self.lock_img = pygame.image.load("gfx/lock.png").convert_alpha ()
        self.bomb_img = pygame.image.load("gfx/bomb.png").convert_alpha ()
        self.gem_img = pygame.image.load("gfx/gem.png").convert_alpha ()
        self.cig_img = pygame.image.load("gfx/cig.png").convert_alpha ()
        self.pistol_img =pygame.image.load("gfx/pistol.png").convert_alpha ()
        self.boss_img = pygame.image.load("gfx/boss.png").convert_alpha ()

        self.cursor_img = pygame.image.load("gfx/cursor.png").convert_alpha ()

        # Позиция камеры
        self.camera_x = 0
        self.camera_y = 0

        # Список врагов
        self.enemies = []
        self.resources = []
        self.spawn_point = []

        #инвентарь
        self.inventory = []
        self.score = 0
        self.happening_text = ''
        self.console_text = ''

        # Проверка спавна
        self.lock_spawned = 0
        self.key_spawned = 0
        self.amulet_spawned = 0
        self.hero_spawned = 0
        self.cig_spawned = 0
        self.pistol_spawned = 0
        
        self.boss_spawns = 0 #при 1 генерирует босса
        self.hero_has_pistol = 0

        self.inv_enter_from_menu = 0


    def spawn_enemy(self, enemy_type, landscape): #теперь эта функция спавнит всё, что может заспавниться на уровне
        x = random.randint(0, 2560)
        y = random.randint(0, 2304)

        # Проверка на пересечение с каждым сегментом горных массивов
        if not any(pygame.Rect(x, y, 32, 32).colliderect(segment) 
                for cluster in landscape.mountains for segment in cluster):
            if enemy_type == "hero":
                    self.hero_spawned = 1
                    self.spawn_point.append (x)
                    self.spawn_point.append (y)
            elif enemy_type == "archer":
                self.enemies.append(EnemyArcher(hp=100, power=20, x=x, y=y, speed=4, protect=5, fov_radius=250, active=1))
            elif enemy_type == "melee":
                self.enemies.append(EnemyMelee(hp=100, power=20, x=x, y=y, speed=random.randint(3, 8), protect=5, fov_radius=300, active=1)) #рандомная скорость для чертей, чтобы было веселее)
            elif enemy_type == "healthpack":
                self.resources.append(HealthPack(hp=10, power=0, x=x, y=y, speed=0, active=1))
            elif enemy_type == "energypack":
                self.resources.append(EnergyPack(hp=0, power=10, x=x, y=y, speed=0, active=1))
            elif enemy_type == "key":
                self.resources.append(Key(hp=0, power=0, x=x, y=y, speed=0, active=1))
                self.key_spawned = 1
                print ('key spawned at ', x, ' ', y)
            elif enemy_type == "lock":
                self.resources.append(Lock(hp=0, power=0, x=x, y=y, speed=0, active=1))
                self.lock_spawned = 1
                print ('lock spawned at ', x, ' ', y)
            elif enemy_type == "amulet":
                self.resources.append(Amulet(hp=0, power=0, x=x, y=y, speed=0, active=1))
                self.amulet_spawned = 1
                #print ('amulet spawned at ', x, ' ', y)
            elif enemy_type == "gem":
                self.resources.append(Gem(hp=0, power=0, x=x, y=y, speed=0, active=1))
                #print ('gem spawned at ', x, ' ', y)
            elif enemy_type == "cig":
                self.resources.append(Cig(hp=0, power=0, x=x, y=y, speed=0, active=1))
                self.cig_spawned = 1
                #print ('cig spawned at ', x, ' ', y)

    def moveCharacter(self, hero, landscape):
        keys = pygame.key.get_pressed()
        hero_rect = pygame.Rect(hero.x, hero.y, 32, 32)
        old_x, old_y = hero.x, hero.y

        if keys[pygame.K_w]:
            new_rect = hero_rect.move(0, -hero.speed)
            if not (any(new_rect.colliderect(segment) for cluster in landscape.mountains for segment in cluster) or (hero.y < 1)):
                hero.y -= hero.speed

        if keys[pygame.K_s]:
            new_rect = hero_rect.move(0, hero.speed)
            if not (any(new_rect.colliderect(segment) for cluster in landscape.mountains for segment in cluster)):
                hero.y += hero.speed

        if keys[pygame.K_a]:
            new_rect = hero_rect.move(-hero.speed, 0)
            if not (any(new_rect.colliderect(segment) for cluster in landscape.mountains for segment in cluster) or (hero.x < 1)):
                hero.x -= hero.speed

        if keys[pygame.K_d]:
            new_rect = hero_rect.move(hero.speed, 0)
            if not (any(new_rect.colliderect(segment) for cluster in landscape.mountains for segment in cluster)):
                hero.x += hero.speed

        # Обновляем позицию камеры
        self.camera_x = hero.x - self.SCREEN_WIDTH // 2
        self.camera_y = hero.y - self.SCREEN_HEIGHT // 2
        self.camera_x = max(0, self.camera_x)  # Ограничиваем камеру по x
        self.camera_y = max(0, self.camera_y)  # Ограничиваем камеру по y

    def playerShoot (self, hero):

        if self.hero_has_pistol == 1:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.shoot_sound.play ()
                    hero.shoot (1)
                if event.key == pygame.K_UP:
                    self.shoot_sound.play ()
                    hero.shoot (4)
                if event.key == pygame.K_RIGHT:
                    self.shoot_sound.play ()
                    hero.shoot (3)
                if event.key == pygame.K_DOWN:
                    self.shoot_sound.play ()
                    hero.shoot (2)

    def togglePause (self): #включает экран паузы
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                states.gameplay_screen = 0
                states.pause_screen = 1

    def toggleInventory (self): #включает экран паузы
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.select_sound.play()
                states.gameplay_screen = 0
                states.inventory_screen = 1

    def toggleConsole (self): #КОНСОЛЬ!!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SLASH:
                self.select_sound.play()
                states.gameplay_screen = 0
                states.console_screen = 1

    def consoleListen (self, text): #тут поправить ссылки на переменные
        if event.type == pygame.KEYDOWN:
            print(f"Key {pygame.key.name(event.key)} pressed")
            if event.key == pygame.K_SPACE:
                dungeon.console_text += ' '
            elif event.unicode.isalnum ():
                dungeon.console_text += str(pygame.key.name(event.key))
            elif event.key == pygame.K_BACKSPACE:
                dungeon.console_text = dungeon.console_text[:-1]
                menu.tileBackground (menu.brick)
            elif event.key == pygame.K_RETURN:
                dungeon.console_text = dungeon.console_text.split (' ')
                if dungeon.console_text[0] == 'tp': #телепортация в формате "tp 123 123"
                    try:
                        level_one.hero.x = int(dungeon.console_text[1])
                        level_one.hero.y = int(dungeon.console_text[2])
                        self.happening_text = 'teleported'
                    except (IndexError, ValueError):
                        print ('значения неправильные')
                if dungeon.console_text[0] == 'hp': #дать полный hp
                    level_one.hero.hp = 100
                    self.happening_text= 'health full'
                if dungeon.console_text[0] == 'power': #дать полный pwr
                    level_one.hero.power = 20
                    self.happening_text = 'power full'
                if dungeon.console_text[0] == 'give': #например "give pistol"
                    if (dungeon.console_text[1] in ['pistol', 'amulet', 'key']) and not (dungeon.console_text[1] in self.inventory):
                        self.inventory.append (dungeon.console_text[1])
                        if (dungeon.console_text[1] == 'pistol'):
                            self.hero_has_pistol = 1

    def tileBackground(self, texture) -> None:
        t_s = pygame.transform.scale (texture, (32,32))
        for x in range(self.tilesX):
            for y in range(self.tilesY):
                self.displaysurf.blit(t_s, (x * 32, y * 32))

    def drawShadow (self, playerx, playery) -> None: #функция для фонарика
        self.shadowsurf.fill ((0,0,0))
        pygame.draw.circle (self.shadowsurf, (255, 255, 255), (level_one.hero.x - self.camera_x, level_one.hero.y - self.camera_y), 200, 0)
        pygame.draw.circle (self.shadowsurf, (0, 0, 0, 128), (level_one.hero.x - self.camera_x, level_one.hero.y - self.camera_y), 200, 0)
        pygame.draw.circle (self.shadowsurf, (255, 255, 255), (level_one.hero.x - self.camera_x, level_one.hero.y - self.camera_y), 100, 0)
        self.displaysurf.blit (self.shadowsurf, (0,0))

    def renderHero(self, hero):
        #pygame.draw.rect(self.displaysurf, color, pygame.Rect(hero.x - self.camera_x, hero.y - self.camera_y, 32, 32))
        if hero.hp > 75:
            self.displaysurf.blit (self.hero_img, ((hero.x - self.camera_x, hero.y - self.camera_y)))
        elif hero.hp > 25:
            self.displaysurf.blit (self.sceptical_img, ((hero.x - self.camera_x, hero.y - self.camera_y)))
        else:
            self.displaysurf.blit (self.crying_img, ((hero.x - self.camera_x, hero.y - self.camera_y)))

    def renderEnemy(self, image, enemy):
        #pygame.draw.rect(self.displaysurf, color, pygame.Rect(enemy.x - self.camera_x, enemy.y - self.camera_y, 32, 32))
        if enemy.active:
            self.displaysurf.blit (image, ((enemy.x - self.camera_x, enemy.y - self.camera_y)))
        if enemy.hp < 100:
            pygame.draw.rect(self.displaysurf, self.L_GREEN, pygame.Rect(enemy.x - self.camera_x, enemy.y - self.camera_y - 8, int(0.32 * enemy.hp), 5))
            

    def renderResource (self, image, resource): #рисует ресурсы
        if (resource.active > 0):
            self.displaysurf.blit (image, ((resource.x - self.camera_x, resource.y - self.camera_y)))

    def renderBullet(self, color, bullet):
        pygame.draw.rect(self.displaysurf, color, pygame.Rect(bullet.x - self.camera_x, bullet.y - self.camera_y, 8, 8))

    def renderStats (self, hp, power): #рисует HP и PWR
        pygame.draw.rect(self.displaysurf, self.L_GREEN, pygame.Rect(16, 16, hp*2, 32))
        pygame.draw.rect(self.displaysurf, self.YELLOW, pygame.Rect(240, 16, power * 10, 32))
        self.displaysurf.blit (self.font_medium.render (str(hp) + ' HP', False, self.GREEN), (16, 16))
        self.displaysurf.blit (self.font_medium.render (str(power) + ' PWR', False, self.BLACK), (240, 16))
        self.displaysurf.blit (self.font_medium.render ('Score: ' + str(self.score), False, self.WHITE), (992, 16))

    def happeningText (self): #выводит лог события
        self.displaysurf.blit (self.font_medium.render (self.happening_text, False, self.WHITE), (992, 48))

    def renderCoordinates (self, x, y):
        self.displaysurf.blit (self.font_medium.render ('x: '+ str(x) + ', y: ' + str(y), False, self.WHITE), (32, 704))

    """def renderCursor (self, x, y):
        self.displaysurf.blit (self.cursor_img, (x, y))"""

    def checkGameOver (self, hero):

        if hero.hp <= 0:
            states.gameplay_screen = 0
            states.game_over_screen = 1

    def renderInventory (self, inventory): #рисует предметы инвентаря

        for i in range (len (self.inventory)):
            if inventory[i] == 'key':
                self.displaysurf.blit (self.key_img, ((320 + 32*i, 448)))
            elif inventory[i] == 'amulet':
                self.displaysurf.blit (self.amulet_img, ((320 + 32*i, 448)))
            elif inventory[i] == 'pistol':
                self.displaysurf.blit (self.pistol_img, ((320 + 32*i, 448)))
            else:
                pass


class LevelOne (GlobalSettings): #тут генерируется ландшафт, координаты игрока, противники, предметы

    def __init__ (self, Hero, EnemyMelee, EnemyArcher, Landscape):
        self.lock_spawned = 0
        self.key_spawned = 0
        self.amulet_spawned = 0
        self.hero_spawned = 0
        self.cig_spawned = 0


        dungeon.score = 0
        dungeon.inventory = []
        dungeon.happening_text = ''
        dungeon.hero_has_pistol = 0

        """#курсор
        self.cursor = Cursor (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])"""

        # Создание ландшафта
        self.landscape = Landscape(2560, 2304)  # Увеличиваем размеры ландшафта
        self.landscape.generate_mountains(random.randint(10, 150))  # Генерация от 10 до 150 гор
        self.landscape.generate_borders ()

        # Спавним случайное количество врагов
        for _ in range(random.randint(5, 10)): # Генерация от 5 до 15 врагов
            if random.choice(["melee", "archer"]) == "melee":
                dungeon.spawn_enemy("melee", self.landscape)
            else:
                dungeon.spawn_enemy("archer", self.landscape)

        # Спавним случайное количество ресурсов
        for _ in range(random.randint(5, 10)):  # Генерация от 5 до 10 ресурсов
            if random.choice(["healthpack", "energypack"]) == "healthpack":
                dungeon.spawn_enemy("healthpack", self.landscape)
            else:
                dungeon.spawn_enemy("energypack", self.landscape)

        for _ in range(random.randint(10, 40)):
            dungeon.spawn_enemy ("gem", self.landscape)

        #не забыть сюда добавлять новые ресурсы
        dungeon.spawn_enemy ("key", self.landscape)
        dungeon.spawn_enemy ("lock", self.landscape)
        dungeon.spawn_enemy ("amulet", self.landscape)
        dungeon.spawn_enemy ("cig", self.landscape)
        dungeon.spawn_enemy ("pistol", self.landscape)
        for _ in range(random.randint(5, 10)):
            dungeon.spawn_enemy ("hero", self.landscape)
        
# Создание главного героя
        self.hero = Hero(hp=100, power=20, x=dungeon.spawn_point[0], y=dungeon.spawn_point[1], speed=6, protect=5, active=1)  # Начальная позиция героя в центре


    def restart (self): #всё генерируется заново при рестарте

        self.lock_spawned = 0
        self.key_spawned = 0
        self.amulet_spawned = 0
        self.hero_spawned = 0
        self.cig_spawned = 0

        dungeon.score = 0
        dungeon.inventory = []
        dungeon.happening_text = ''
        dungeon.hero_has_pistol = 0

        # Список врагов
        dungeon.enemies = []
        dungeon.resources = []
        dungeon.spawn_point = []

        """#курсор
        self.cursor = Cursor (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])"""

        # Создание ландшафта
        self.landscape = Landscape(2560, 2304)  # Увеличиваем размеры ландшафта
        self.landscape.generate_mountains(random.randint(50, 150))  # Генерация от 10 до 150 гор
        self.landscape.generate_borders ()

        # Спавним случайное количество врагов
        for _ in range(random.randint(15, 45)):  # Генерация от 5 до 15 врагов
            if random.choice(["melee", "archer"]) == "melee":
                dungeon.spawn_enemy("melee", self.landscape)
            else:
                dungeon.spawn_enemy("archer", self.landscape)

        # Спавним случайное количество ресурсов
        for _ in range(random.randint(5, 20)):  # Генерация от 5 до 20 ресурсов
            if random.choice(["healthpack", "energypack"]) == "healthpack":
                dungeon.spawn_enemy("healthpack", self.landscape)
            else:
                dungeon.spawn_enemy("energypack", self.landscape)

        for _ in range(random.randint(10, 40)):
            dungeon.spawn_enemy ("gem", self.landscape)

        dungeon.spawn_enemy ("key", self.landscape)
        dungeon.spawn_enemy ("lock", self.landscape)
        dungeon.spawn_enemy ("amulet", self.landscape)
        dungeon.spawn_enemy ("cig", self.landscape)
        dungeon.spawn_enemy ("pistol", self.landscape)
        for _ in range(random.randint(5, 10)):
            dungeon.spawn_enemy ("hero", self.landscape)

        # Создание главного героя
        self.hero = Hero(hp=100, power=20, x=dungeon.spawn_point[0], y=dungeon.spawn_point[1], speed=6, protect=5, active=1)  # Начальная позиция героя в центре

        # Позиция камеры
        dungeon.camera_x = 0
        dungeon.camera_y = 0


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.display.set_caption("Dungeon Sandbox")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    states = States ()
    dungeon = Gameplay()
    pause = PauseMenu ()
    menu = StartMenu ()
    level_one = LevelOne (Hero, EnemyMelee, EnemyArcher, Landscape)

    pygame.display.set_icon(pygame.transform.scale(pygame.image.load('gfx/brick.png'), (32,32)))

    while True:



        while states.menu_screen: #главный экран
            dungeon.tileBackground (dungeon.brick)
            for event in pygame.event.get():
                menu.quitGame ()
                menu.scroll ()
                menu.pressReturn ()
            menu.drawLogo ()
            menu.drawButtons (menu.btn_count)
            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)




        while states.help_screen: #экран по кнопке help
            menu.tileBackground (menu.brick)
            menu.displaysurf.blit (menu.font_medium.render ('Найди пистолет и разберись с чертями!', False, menu.WHITE, menu.SHADOW), (240, 240))
            menu.btn_count = 0
            menu.ok_btn.update(0)
            menu.displaysurf.blit(menu.ok_btn.surf, menu.ok_btn.origin)
            for event in pygame.event.get():
                menu.quitGame ()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu.select_sound.play()
                        states.menu_screen = 1
                        states.help_screen = 0
                        menu.btn_count = 1

            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)




        if states.gameplay_screen: #запуск новой игры
            states.times_pause = 0
            if states.restart == 1:
                level_one.restart ()
            while True:
                if not (dungeon.key_spawned == 1 and dungeon.hero_spawned == 1 and dungeon.lock_spawned == 1 and dungeon.amulet_spawned == 1 and dungeon.cig_spawned == 1): #проверка того, что все нужные вещи заспавнились
                    level_one.restart ()
                else:
                    break
        while states.gameplay_screen: #основной геймплейный луп

            dt = pygame.time.get_ticks()
            for event in pygame.event.get():
                dungeon.quitGame()
                dungeon.togglePause ()
                dungeon.toggleInventory ()
                dungeon.toggleConsole ()
                dungeon.playerShoot (level_one.hero)
                """if dt2 > 500:
                    level_one.hero.updatePower ()
                    dt2 = 0"""

            #проверяем здоровьe
            dungeon.checkGameOver (level_one.hero)

            # Отрисовка фона
            dungeon.tileBackground(dungeon.brick)
            
            # Обновление позиции героя
            dungeon.moveCharacter(level_one.hero, level_one.landscape)

            #обновление ресурсов
            for resource in dungeon.resources:
                resource.update(level_one.hero, dungeon)  

            # Обновление врагов
            for enemy in dungeon.enemies:
                if enemy.active:
                    enemy.update(level_one.hero, level_one.landscape)  # Передаём героя
    
                    # Обновление и отрисовка пуль, с проверкой таймера на уничтожение
                    if isinstance(enemy, EnemyArcher) and enemy.bullet and enemy.bullet.update(dungeon, level_one.hero):
                        dungeon.renderBullet(dungeon.WHITE, enemy.bullet)
                    else:
                        enemy.bullet = None  # Удаляем пулю, если она "умерла"
                else:
                    dungeon.enemies.remove (enemy)
                    enemy.spawnResource (EnergyPack(hp=0, power=10, x=enemy.x, y=enemy.y, speed=0, active=1), dungeon)
                    dungeon.die_sound.play ()
    
            # Отрисовка ландшафта с учетом камеры
            level_one.landscape.draw(dungeon.displaysurf, dungeon.camera_x, dungeon.camera_y)
            dungeon.drawShadow (level_one.hero.x, level_one.hero.y)
    
            # Отрисовка всех объектов на экране
            dungeon.renderHero(level_one.hero)
            if level_one.hero.bullet and level_one.hero.bullet.update():
                dungeon.renderBullet(dungeon.WHITE, level_one.hero.bullet)


            for enemy in dungeon.enemies:
                if (abs(level_one.hero.x-enemy.x) < 200) and (abs(level_one.hero.y - enemy.y) < 200):
                    if isinstance(enemy, EnemyMelee):
                        dungeon.renderEnemy(dungeon.melee_img, enemy)
                    elif isinstance(enemy, EnemyArcher):
                        dungeon.renderEnemy(dungeon.archer_img, enemy)

            for resource in dungeon.resources: #рендер ресурсов
                if (abs(level_one.hero.x-resource.x) < 200) and (abs(level_one.hero.y - resource.y) < 200):
                    if isinstance(resource, HealthPack):
                        dungeon.renderResource(dungeon.health_img, resource)
                    elif isinstance(resource, EnergyPack):
                        dungeon.renderResource(dungeon.energy_img, resource)
                    elif isinstance(resource, Lock):
                        dungeon.renderResource(dungeon.lock_img, resource)
                    elif isinstance(resource, Key):
                        dungeon.renderResource(dungeon.key_img, resource)    
                    elif isinstance(resource, Amulet):
                        dungeon.renderResource(dungeon.amulet_img, resource)
                    elif isinstance(resource, Gem):
                        dungeon.renderResource(dungeon.gem_img, resource)
                    elif isinstance(resource, Pistol):
                        dungeon.renderResource(dungeon.pistol_img, resource)
                    elif isinstance(resource, Gem):
                        dungeon.renderResource(dungeon.cig_img, resource)

            dungeon.renderStats (level_one.hero.hp, level_one.hero.power)
            dungeon.happeningText ()
            dungeon.renderCoordinates (level_one.hero.x, level_one.hero.y)
            # Обновление экрана
            pygame.display.flip()
    
            # Ограничение FPS
            clock.tick(dungeon.FPS)


        if states.pause_screen and states.times_pause == 0: #затемнение экрана при паузе
            menu.select_sound.play()
            dungeon.tileBackground (dungeon.shadow_img) #это сделать получше
            dungeon.tileBackground (dungeon.shadow_img)
            pause_gfx = PauseGfx (dungeon.displaysurf.copy ())  
            states.times_pause = 1  
            states.restart = 0
            pause.btn_count = 0
        else:
            pause_gfx = PauseGfx (dungeon.displaysurf.copy ())
            states.restart = 0


        while states.pause_screen: #экран паузы
            for event in pygame.event.get():
                pause.quitGame ()
                pause.scroll ()
                pause.pressReturn ()
            pause.drawButtons (pause.btn_count)
            pygame.display.flip()
            pause.FramePerSec.tick(pause.FPS)



        while states.inventory_screen: #экран инвентаря
            menu.tileBackground (menu.brick)
            menu.displaysurf.blit (menu.font_big.render ('инвентарь', False, menu.WHITE), (320, 32))
            menu.btn_count = 0
            menu.ok_btn.update(0)
            menu.displaysurf.blit(menu.ok_btn.surf, menu.ok_btn.origin)
            dungeon.renderInventory (dungeon.inventory)
            for event in pygame.event.get():
                menu.quitGame ()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i or event.key == pygame.K_RETURN:
                        menu.select_sound.play()
                        states.gameplay_screen = 1
                        states.inventory_screen = 0
                        pause.btn_count = 1
                        menu.displaysurf.blit (pause_gfx.x, (0,0))

            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)


        if states.game_over_screen:
            menu.player_die_sound.play ()
        while states.game_over_screen: #экран game over при смерти
            menu.displaysurf.fill ((0,0,0))
            menu.displaysurf.blit (menu.font_bigger.render ('GAME OVER', False, menu.WHITE), (240, 240))
            menu.btn_count = 0
            menu.ok_btn.update(0)
            menu.displaysurf.blit(menu.ok_btn.surf, menu.ok_btn.origin)
            for event in pygame.event.get():
                menu.quitGame ()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu.select_sound.play()
                        states.menu_screen = 1
                        states.game_over_screen = 0
                        menu.btn_count = 1

            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)



        if states.console_screen:
            menu.tileBackground (menu.brick)
        while states.console_screen: #экран по кнопке help
            menu.displaysurf.blit (menu.font_big.render ('CONSOLE', False, menu.WHITE), (320, 32))
            for event in pygame.event.get():
                menu.quitGame ()
                dungeon.consoleListen (dungeon.console_text)
                if event.type == pygame.KEYDOWN:
                    menu.displaysurf.blit (dungeon.font_medium.render (' '.join(map(str, dungeon.console_text)), False, menu.WHITE, menu.SHADOW), (320, 448))
                    if event.key == pygame.K_SLASH or event.key == pygame.K_RETURN:
                        menu.select_sound.play()
                        states.gameplay_screen = 1
                        states.console_screen = 0
                        dungeon.console_text = ''
            pygame.display.flip()
            menu.FramePerSec.tick(menu.FPS)
