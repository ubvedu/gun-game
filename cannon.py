import math
import pygame
from colors import GREY, RED, DARK_GREY
from ball import Ball
from utils import draw_rotated


class Cannon:
    def __init__(self, screen):
        self.screen = screen
        self.power = 10
        self.preparing = 0
        self.angle = 1
        self.color = GREY

        self.ball_r = 16
        self.h2 = self.ball_r * 2 + 2
        self.h1 = int(self.h2 * 4 / 3)
        self.w = self.h1 * 2

        self.power_default = 0.1
        self.power_increase = 0.02
        self.power_max = 1
        self.release()

        self.x = self.h1 / 2
        self.y = self.screen.get_clip().h / 2

        self.vy = 0

    def move(self):
        self.y = min(max(0, self.y + self.vy), self.screen.get_clip().h)

    def release(self):
        self.preparing = False
        self.power = self.power_default

    def prepare(self):
        """
        Подготовка к выстрелу.

        Происходит при нажатии мыши. Во время подготовки контролируется сила выстрела.
        """
        self.preparing = True

    def fire(self):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.

        :return: выстреленный мяч
        """
        lever = self.w - self.h1
        v = 100
        ball = Ball(
            self.screen,
            self.x + lever * math.cos(self.angle),
            self.y + lever * math.sin(self.angle),
            20,
            v * self.power * math.cos(self.angle),
            v * self.power * math.sin(self.angle)
        )
        self.release()
        return ball

    def target(self, event):
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

        sf = pygame.Surface((self.w, self.h1))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.polygon(sf, GREY, [
            (self.h1 / 2, 0),
            (self.h1 / 2, self.h1),
            (self.w, (self.h1 + self.h2) / 2),
            (self.w, (self.h1 - self.h2) / 2),
        ])
        draw_rotated(self.screen, self.x, self.y, sf, self.h1 / 2, self.h1 / 2, self.angle)

        sf = pygame.Surface((self.w, self.h1))
        sf.set_colorkey((0, 0, 0))
        p = self.power - self.power_default
        x = p * (self.h1 / 2 - self.w) + self.w
        d = (1 - p) * (self.h1 - self.h2) / 2
        pygame.draw.polygon(sf, RED, [
            (x, d),
            (x, self.h1 - d),
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
        if self.preparing and self.power < self.power_max:
            self.power += self.power_increase
