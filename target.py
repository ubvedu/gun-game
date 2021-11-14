import pygame
from random import random, randint
from colors import LIGHT_BLUE, BLACK
from utils import draw_rotated
import math


def target_xy(clip, targets):
    target_r = 60
    while True:
        x = randint(clip.w / 2, clip.w)
        y = randint(0, clip.h)
        legal = True
        for t in targets:
            if (x - t.x) ** 2 + (y - t.y) ** 2 < (target_r * 2) ** 2:
                legal = False
        if legal:
            return x, y


ENTERING, ACTIVE, EXITING, DEAD = range(4)


class Target:

    def __init__(self, screen, targets):
        """ Инициализация новой цели. """
        self.angle = (1 + random()) * math.pi / 2
        self.omega = (random() - 0.5) * math.pi / 32
        self.w = 120
        self.h = 16
        self.color = LIGHT_BLUE
        self.color_ax = BLACK
        self.screen = screen

        self.x, self.y = target_xy(screen.get_clip(), targets)
        self.y_temp = -self.w
        self.y_step = 5

        self.state = ENTERING
        self.steps = 0
        self.max_steps = 100

    def move(self):
        if self.state == ENTERING:
            self.y_temp += self.y_step
            if self.y_temp > self.y:
                self.state = ACTIVE
        elif self.state == ACTIVE:
            self.angle += self.omega
            self.steps += 1
            if self.steps > self.max_steps:
                self.state = EXITING
        elif self.state == EXITING:
            self.y_temp += self.y_step
            if self.y_temp > self.screen.get_clip().h + self.w:
                self.state = DEAD

    def hit(self, points=1):
        """Попадание шарика в цель."""

    def draw(self):
        sf = pygame.Surface((self.w, self.h))
        sf.set_colorkey((0, 0, 0))
        color = self.color
        if self.state != ACTIVE:
            color += '40'
        pygame.draw.rect(sf, color, (0, 0, self.w, self.h))
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
