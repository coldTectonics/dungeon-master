import math
import pygame, sys
from pygame.locals import *
import numpy as np
import random

class Entity:
    def __init__(self, hp, power, x, y, speed, active) -> None:
        self.hp = hp
        self.power = power
        self.speed = speed
        self.x = x
        self.y = y
        self.active = active

    def spawnResource (self, resource, gameplay): #спавнит лут
        gameplay.resources.append (resource)



class Hero(Entity):
    def __init__(self, hp, power, x, y, speed, protect, active) -> None:
        super().__init__(hp, power, x, y, speed, active)
        self.protect = protect
        self.bullet = None
        self.speed = speed

    def shoot(self, direction):
        if self.power >= 5:
            self.bullet = PlayerBullet(self.x, self.y, direction)
            self.power -= 1

    def updatePower (self):
        if self.power < 15:
            self.power += 5
        else: 
            self.power = 20
                
                
class SimpleNeuralNet:
    def __init__(self, input_size=4, hidden_size=6, output_size=2):
        self.weights = {
            'w1': np.random.randn(input_size, hidden_size),
            'b1': np.random.randn(hidden_size),
            'w2': np.random.randn(hidden_size, output_size),
            'b2': np.random.randn(output_size)
        }

    def forward(self, inputs):
        z1 = np.dot(inputs, self.weights['w1']) + self.weights['b1']
        a1 = np.tanh(z1)
        z2 = np.dot(a1, self.weights['w2']) + self.weights['b2']
        return np.tanh(z2)

                

class EnemyMelee(Entity):
    def __init__(self, hp, power, x, y, speed, protect, fov_radius, active):
        super().__init__(hp, power, x, y, speed, active)
        self.damage = 7
        self.protect = protect
        self.fov_radius = fov_radius
        self.is_moving = False
        self.neural_net = SimpleNeuralNet()
        self.direction = np.array([random.choice([-1, 1]), random.choice([-1, 1])])  # Начальное направление
        self.step_counter = 0
        self.change_direction_interval = 20  # Сколько шагов идти в одном направлении
        self.move_delay = 20  # Задержка между движениями (количество кадров)
        self.move_timer = 0  # Таймер для отслеживания времени движения

    def update(self, hero, landscape):
        dx, dy = hero.x - self.x, hero.y - self.y
        distance_to_hero = math.hypot(dx, dy)

        inputs = np.array([self.x, self.y, hero.x, hero.y])

        if distance_to_hero <= self.fov_radius:
            # Если герой в поле зрения, враг начинает двигаться к нему
            self.is_moving = True
            dx, dy = dx / distance_to_hero, dy / distance_to_hero
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
        else:
            self.is_moving = False
            
            # Используем нейронку для получения движения
            move_decision = self.neural_net.forward(inputs)

            # Плавное случайное движение
            if self.step_counter < self.change_direction_interval:
                # Проверяем, пришло ли время движения
                if self.move_timer <= 0:
                    new_x = self.x + self.direction[0] * self.speed * 0.5  # Уменьшаем скорость
                    new_y = self.y + self.direction[1] * self.speed * 0.5  # Уменьшаем скорость
                    self.move_timer = self.move_delay  # Сбрасываем таймер
                else:
                    new_x, new_y = self.x, self.y  # Остаёмся на месте
                    self.move_timer -= 1  # Уменьшаем таймер
                self.step_counter += 1
            else:
                # Меняем направление
                self.direction = np.array([random.choice([-1, 1]), random.choice([-1, 1])])
                new_x = self.x + self.direction[0] * self.speed * 0.5
                new_y = self.y + self.direction[1] * self.speed * 0.5
                self.move_timer = self.move_delay  # Сбрасываем таймер
                self.step_counter = 0

        new_rect = pygame.Rect(new_x, new_y, 32, 32)
        if not any(new_rect.colliderect(segment) for cluster in landscape.mountains for segment in cluster):
            self.x, self.y = new_x, new_y
        else:
            # Если есть препятствие, меняем направление
            self.direction = np.array([random.choice([-1, 1]), random.choice([-1, 1])])

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32)): #урон при коллижне
            hero.hp -= self.damage

        if hero.bullet and (pygame.Rect(self.x, self.y, 32, 32).colliderect(hero.bullet.x, hero.bullet.y, 8, 8)): #урон при коллижне
            self.hp -= 20
            hero.bullet = None

        if self.hp <= 0:
            self.active = 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 20)

class EnemyArcher(Entity):
    def __init__(self, hp, power, x, y, speed, protect, fov_radius, active) -> None:
        super().__init__(hp, power, x, y, speed, active)
        self.protect = protect
        self.fov_radius = fov_radius  # Поле зрения лучника
        self.shoot_delay = 1000 
        self.last_shot = pygame.time.get_ticks() 
        self.bullet = None  # Изначально пуля отсутствует
        self.damage = 2

    def update(self, hero, landscape):  # Добавляем landscape как аргумент
        # Вычисляем расстояние до героя
        dx, dy = hero.x - self.x, hero.y - self.y
        distance_to_hero = math.hypot(dx, dy)

        # Если герой в пределах поля зрения, пытаемся стрелять
        if distance_to_hero <= self.fov_radius:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.shoot()
                self.last_shot = now

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32)): #урон при коллижне
            hero.hp -= self.damage

        if hero.bullet and (pygame.Rect(self.x, self.y, 32, 32).colliderect(hero.bullet.x, hero.bullet.y, 8, 8)): #урон при коллижне
            self.hp -= 20
            hero.bullet = None

        if self.hp <= 0:
            self.active = 0

    def shoot(self):
        print('archer shot')
        self.bullet = Bullet(self.x, self.y, math.radians(90))  # Создаём новую пулю

    def draw(self, screen):
        # Отрисовка лучника
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), 20)
        # Отрисовка пули, если она существует
        if self.bullet:
            self.bullet.draw(screen)  # Предполагается, что метод draw() есть у класса Bullet

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 3
        self.direction = direction
        self.creation_time = pygame.time.get_ticks()  # Время создания пули

    def update(self, dungeon, hero):
        # Проверяем, прошло ли 3 секунды с момента создания пули
        if pygame.time.get_ticks() - self.creation_time > 800:
            return False  # Пуля "умирает" через 3 секунды
        
        dx, dy = hero.x - self.x, hero.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist 
        self.x += dx * self.speed
        self.y += dy * self.speed

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 8, 8)):
            hero.hp -= 10
            return False

        return True  # Пуля продолжает существовать

class PlayerBullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 8
        self.direction = direction
        self.creation_time = pygame.time.get_ticks() 

    def update (self):
        if pygame.time.get_ticks() - self.creation_time > 800:
            return False

        if self.direction == 1: #лево
            self.x -= self.speed
        if self.direction == 2: #низ
            self.y += self.speed
        if self.direction == 3: #право
            self.x += self.speed
        if self.direction == 4: #верх
            self.y -= self.speed
        if self.direction == 12: #левониз
            self.x -= self.speed
            self.y += self.speed
        if self.direction == 32: #правониз
            self.x += self.speed
            self.y += self.speed
        if self.direction == 14: #левоверх
            self.x -= self.speed
            self.y -= self.speed
        if self.direction == 34: #правоверх
            self.x += self.speed
            self.y -= self.speed

        return True

class HealthPack (Entity): #восстанавливает hp
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)
        self.hp = hp
        self.power = power
        self.speed = speed
        self.x = x
        self.y = y
        
    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            if hero.hp < 90:
                hero.hp += 10
            else: 
                hero.hp = 100

            gameplay.happening_text = '+10 hp'



class EnergyPack (Entity): #восстанавливает power
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            hero.power = 20

            gameplay.happening_text = 'full energy'


class Amulet (Entity): #амулет
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):
        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            gameplay.inventory.append ('amulet')
            gameplay.happening_text = 'got amulet'


class Key (Entity): #ключ
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            gameplay.inventory.append ('key')
            gameplay.happening_text = 'got key'


class Lock (Entity): #замок
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1) and ('key' in gameplay.inventory)): #открывается только с ключом
            self.active = 0
            gameplay.scroll_sound.play()
            gameplay.inventory.remove ('key') #удаляет из инвентаря ключ
            self.spawnResource (Pistol(hp=0, power=0, x=self.x, y=self.y, speed=0, active=1), gameplay)
            gameplay.happening_text = 'lock opened'

class Gem (Entity): #кристалл
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)
        self.score = 100

    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            gameplay.score += self.score #прибавляем очки
            gameplay.happening_text = 'got gem'

class Pistol (Entity): #пистолет
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):
        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.scroll_sound.play()
            gameplay.hero_has_pistol = 1
            gameplay.inventory.append ('pistol')
            gameplay.happening_text = 'got pistol'

class Cig (Entity): #сигарета
    def __init__(self, hp, power, x, y, speed, active) -> None:
        super().__init__(hp, power, x, y, speed, active)

    def update(self, hero, gameplay):

        if (pygame.Rect(hero.x, hero.y, 32, 32).colliderect(self.x, self.y, 32, 32) and (self.active == 1)):
            self.active = 0
            gameplay.boss_spawns = 1
            gameplay.happening_text = 'got cig!'

"""class Cursor (): #это мог быть кастомный курсор
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]"""
