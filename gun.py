import math
import pygame
from pygame import draw
from colors import GREY, RED, DARK_GREY
from ball import Ball
from utils import draw_rotated


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.power = 10
        self.preparing = 0
        self.angle = 1
        self.color = GREY

        self.x = 40
        self.y = self.screen.get_clip().h / 2

    def prepare(self):
        """
        Подготовка к выстрелу.

        Происходит при нажатии мыши. Во время подготовки контролируется сила выстрела.
        """
        self.preparing = True
        self.power = 10

    def fire(self):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.

        :return: выстреленный мяч
        """

        self.preparing = False

        lever = self.w - self.h1
        return Ball(
            self.screen,
            self.x + lever * math.cos(self.angle),
            self.y + lever * math.sin(self.angle),
            15,
            self.power * math.cos(self.angle),
            self.power * math.sin(self.angle)
        )

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.update_angle(event.pos)
        if self.preparing:
            self.color = RED
        else:
            self.color = GREY

    def update_angle(self, pos):
        """Обновляет угол направления пушки."""
        x, y = pos
        if x - self.x < 0:
            return
        self.angle = math.atan2(y - self.y, x - self.x)

    def draw(self):
        """Рисует мяч на экране."""

        self.w = 100
        self.h1 = 48
        self.h2 = 32

        sf = pygame.Surface((self.w, self.h1))
        sf.set_colorkey((0, 0, 0))
        color = RED if self.preparing else GREY
        pygame.draw.polygon(sf, color, [
            (self.h1 / 2, 0),
            (self.h1 / 2, self.h1),
            (self.w, (self.h1 + self.h2) / 2),
            (self.w, (self.h1 - self.h2) / 2),
        ])
        draw_rotated(self.screen, self.x, self.y, sf, self.h1 / 2, self.h1 / 2, self.angle)    

        r = 48
        sf = pygame.Surface((r, 2*r))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.circle(sf, DARK_GREY, (0, r), r)
        self.screen.blit(sf, (self.x - r / 2, self.y - r))

    def power_up(self):
        if self.preparing and self.power < 100:
            self.power += 1
