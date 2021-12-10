import pygame
from random import random
from colors import LIGHT_BLUE, BLACK, WHITE
from utils import draw_rotated
import math


class SpinnerSpawner:
    def __init__(self, screen) -> None:
        self.screen = screen

        self.cols = [[], []]
        self.col_gap = screen.get_clip().w // 8

        clip = screen.get_clip()
        self.col_x = [
            clip.w // 2 - self.col_gap,
            # clip.w // 2,
            clip.w // 2 + self.col_gap,
        ]

        self.spinner_speed = -3
        self.spawn_modes = 2

        self.spinner_w = 180
        self.spinner_h = 16
        self.spinner_gap = 30

        self.spawn_period = (
            self.spinner_w + self.spinner_gap) / abs(self.spinner_speed) / self.spawn_modes
        self.frames_from_spawn = self.spawn_period
        self.spawn_col_idx = 0

        for _ in range(400):
            self.move()

    def move(self):
        self.frames_from_spawn += 1
        if self.frames_from_spawn > self.spawn_period:
            for i in range(len(self.cols)):
                if i % self.spawn_modes == self.spawn_col_idx:
                    self.cols[i].append(Spinner(
                        self.screen,
                        self.spinner_w,
                        self.spinner_h,
                        self.col_x[i],
                        self.spinner_speed,
                    ))
            self.spawn_col_idx = (self.spawn_col_idx + 1) % self.spawn_modes
            self.frames_from_spawn = 0
        for col in self.cols:
            for target in col:
                target.move()

    def draw(self):
        for col in self.cols:
            for t in col:
                t.draw()

    def nearest_from(self, x, y):
        rx, ry = 10 ** 6, 10 ** 6
        r2 = 10 ** 6
        for col in self.cols:
            for t in col:
                rx_, ry_ = t.nearest_from(x, y)
                r2_ = rx_ ** 2 + ry_ ** 2
                if r2_ < r2:
                    rx = rx_
                    ry = ry_
                    r2 = r2_
        return rx, ry


class Spinner:
    def __init__(self, screen, w, h, x, vy):
        """ Инициализация новой цели. """
        self.angle = (random()) * math.pi * 2
        self.omega = (random() - 0.5) * math.pi / 32
        self.w = w
        self.h = h
        self.color = BLACK
        self.color_ax = WHITE
        self.screen = screen

        self.x = x
        self.y = screen.get_clip().h+self.w
        self.y_speed = vy

    def move(self):
        self.y += self.y_speed
        self.angle += self.omega

    def draw(self):
        sf = pygame.Surface((self.w, self.h))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.rect(sf, self.color, (0, 0, self.w, self.h))
        draw_rotated(self.screen, self.x, self.y, sf,
                     self.w / 2, self.h / 2, self.angle)
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
