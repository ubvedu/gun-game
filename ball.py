import math
import pygame
from colors import DARKER_GREY
from random import choice


class Ball:
    def __init__(self, screen, x, y, r, vx, vy):
        """
        Конструктор класса ball

        :param screen: экран для прорисовки
        :param x: начальное положение мяча по горизонтали
        :param y: начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.g = 1
        self.save_k = 0.8
        self.color = DARKER_GREY
        self.live = 30

    def is_out(self):
        return self.screen.get_clip().h < self.y - self.r

    def move(self):
        """
        Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        self.x += self.vx
        self.vy += self.g
        self.y += self.vy

    def draw(self):
        """
        Отображает мяч на экране.
        """
        pygame.draw.circle(self.screen, self.color, (round(self.x), round(self.y)), self.r)

    def collide(self, obj):
        """
        Проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Если столкновение произошло, меняет кинематические характеритики объекта.

        :param obj: Обьект, с которым проверяется столкновение.
        :return: Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        x, y = obj.nearest_from(self.x, self.y)
        dist2 = x ** 2 + y ** 2

        if 0 < dist2 < self.r ** 2:
            self.reflect(x, y)

        return False

    def reflect(self, x, y):
        """
        Отражает скорость относительно данного вектора и меняет на противоположную c потерями энергии.
        """
        dist2 = x ** 2 + y ** 2
        v_proj = self.vx * x + self.vy * y
        px = -v_proj * x / dist2
        py = -v_proj * y / dist2
        self.vx += 2 * px
        self.vy += 2 * py
        self.vx *= self.save_k
        self.vy *= self.save_k

        a = (self.r / math.sqrt(dist2) - 1)
        self.x -= x * a
        self.y -= y * a
