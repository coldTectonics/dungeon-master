import pygame
import random

def draw_entity(screen, entity, x, y):
    color = (0, 128, 0)  # цвет героя
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 50, 50))  # рисуем героя как квадрат 50x50
    

class Landscape:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mountains = []  # Список для хранения всех горных массивов


    def generate_mountains(self, num_mountain_clusters):
        """Генерация массивов гор на карте."""
        for _ in range(num_mountain_clusters):
            # Случайные координаты для центральной позиции горного массива
            base_x = random.randint(0, self.width - 32)
            base_y = random.randint(0, self.height - 32)

            # Создание одного массива гор вокруг точки base_x, base_y
            cluster = []
            for _ in range(random.randint(5, 15)):  # Количество сегментов в массиве
                # Случайное смещение от базовой точки
                offset_x = base_x + random.randint(-64, 64)
                offset_y = base_y + random.randint(-64, 64)

                # Случайный размер сегмента (чтобы добавить разнообразие форм)
                width = random.randint(16, 64)
                height = random.randint(16, 64)

                # Создаем прямоугольник сегмента горного массива
                rect = pygame.Rect(offset_x, offset_y, width, height)
                cluster.append(rect)  # Добавляем сегмент в текущий массив

            self.mountains.append(cluster)  # Добавляем массив в список всех гор

    def generate_borders (self):
        cluster = []
        rect = pygame.Rect (self.width, 0, 250, self.height+250)
        cluster.append (rect)
        rect = pygame.Rect (0, self.height, self.width, 250)
        cluster.append(rect)
        self.mountains.append (cluster)

    def draw(self, screen, camera_x, camera_y):
        """Отрисовка горных массивов на экране."""
        for cluster in self.mountains:
            for segment in cluster:
                # Смещение от камеры
                screen_x = segment.x - camera_x
                screen_y = segment.y - camera_y
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screen_x, screen_y, segment.width, segment.height))  # Коричневый цвет для гор

    def draw_mini_map(self, screen, camera_x, camera_y):
        """Отрисовка горных массивов на экране."""
        for cluster in self.mountains:
            for segment in cluster:

                screen_x = segment.x - camera_x
                screen_y = segment.y - camera_y
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(800, 500, segment.width / 10, segment.height / 10))  # Коричневый цвет для гор
