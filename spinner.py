import pygame
from random import random
from colors import LIGHT_BLUE, BLACK
from utils import draw_rotated
import math


class SpinnerSpawner:
    def __init__(self, screen) -> None:
        self.screen = screen

        self.targets = [[], [], []]
        self.col_gap = 160

        clip = screen.get_clip()
        self.target_x = [
            clip.w // 2 - self.col_gap, 
            clip.w // 2,
            clip.w // 2 + self.col_gap,
        ]
        
        self.spawn_period = 30
        self.frames_from_spawn = self.spawn_period
        self.spawn_col = 0

    def move(self):
        self.frames_from_spawn += 1
        if self.frames_from_spawn > self.spawn_period:
            for (i, (col, x)) in enumerate(zip(self.targets, self.target_x)):
                if i % 2 == self.spawn_col:
                    col.append(Spinner(self.screen, x))
            self.spawn_col = (self.spawn_col + 1) % 2
            self.frames_from_spawn = 0
        for col in self.targets:
            for target in col:
                target.move()

    def draw(self):
        for col in self.targets:
            for t in col:
                t.draw()

    def nearest_from(self, x, y):
        rx, ry = 10 ** 6, 10 ** 6
        r2 = 10 ** 6
        for col in self.targets:
            for t in col:
                rx_, ry_ = t.nearest_from(x, y)
                r2_ = rx_ ** 2 + ry_ ** 2
                if r2_ < r2:
                    rx = rx_
                    ry = ry_
                    r2 = r2_
        return rx, ry


class Spinner:
    def __init__(self, screen, x):
        """ Инициализация новой цели. """
        self.angle = (random()) * math.pi * 2
        self.omega = (random() - 0.5) * math.pi / 32
        self.w = 120
        self.h = 16
        self.color = LIGHT_BLUE
        self.color_ax = BLACK
        self.screen = screen

        self.x = x
        self.y = screen.get_clip().h+self.w
        self.y_speed = -3

    def move(self):
        self.y += self.y_speed
        self.angle += self.omega

    def draw(self):
        sf = pygame.Surface((self.w, self.h))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.rect(sf, self.color, (0, 0, self.w, self.h))
        draw_rotated(self.screen, self.x, self.y, sf, self.w / 2, self.h / 2, self.angle)
        pygame.draw.circle(self.screen, self.color_ax, (self.x, self.y), 2)

    def nearest_from(self, x, y):
        """
        Возвращает вектор, направленный на ближайшую точку цели от заданной.
        """

        # координаты положения центра цели
        dx = self.x - x
        dy = self.y - y
        
        # поперечная нормаль цели
        n1x = -math.sin(self.angle)
        n1y = +math.cos(self.angle)
        
        # продольная нормаль цели
        n2x = +math.cos(self.angle)
        n2y = +math.sin(self.angle)

        # проекции положения центра цели на нормали
        pr1 = n1x * dx + n1y * dy
        pr2 = n2x * dx + n2y * dy

        # искомый вектор в базисе нормалей
        r1 = math.copysign(max(abs(pr1) - self.h / 2, 0), pr1)
        r2 = math.copysign(max(abs(pr2) - self.w / 2, 0), pr2)

        # рассчёт искомого вектора
        return n1x * r1 + n2x * r2, n1y * r1 + n2y * r2

    def reflect(self, x, y):
        pass
