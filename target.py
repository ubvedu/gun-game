import pygame
from random import randint as rnd, random
from colors import LIGHT_BLUE, BLACK
from utils import draw_rotated
import math


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen):
        """ Инициализация новой цели. """
        r = screen.get_clip()
        self.r = rnd(2, 50)
        self.angle = (1 + random()) * math.pi / 2
        self.omega = random() * math.pi / 32
        self.w = 120
        self.h = 16
        self.color = LIGHT_BLUE
        self.color_ax = BLACK
        self.screen = screen

        self.x = rnd(r.w / 2, r.w)
        self.y = rnd(self.w / 2, r.h - self.w / 2)

    def move(self):
        self.angle += self.omega

    def hit(self, points=1):
        """Попадание шарика в цель."""

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
        proj1 = n1x * dx + n1y * dy
        proj2 = n2x * dx + n2y * dy

        # искомый вектор в базисе нормалей
        r1 = math.copysign(max(abs(proj1) - self.h / 2, 0), proj1)
        r2 = math.copysign(max(abs(proj2) - self.w / 2, 0), proj2)

        # рассчёт искомого вектора
        return n1x * r1 + n2x * r2, n1y * r1 + n2y * r2
