import math
from random import randint
from typing import Union
import pygame
from colors import BLACK, BLUE_COLORS, GREY, RED_COLORS
from ball import Ball
from utils import draw_rotated


class Cannon:
    def __init__(self, screen, x, y, team, direction, colors):
        self.screen = screen
        self.angle = 1
        self.body_color = colors[2]
        self.barrel_color = colors[1]
        self.ball_color = colors[0]

        self.team = team

        self.ball_r = 16
        self.r2 = self.ball_r * 2 + 2
        self.r1 = self.r2 * 4 // 3
        self.r0 = self.r1
        self.w = self.r1 * 2

        self.power_default = 0.1
        self.power_increase = 0.02
        self.power_max = 1

        self.preparing = False
        self.power = self.power_default

        self.flipped = direction == -1
        self.sgn = direction

        self.x = x
        self.y = y

        self.vy = 0

    def release(self):
        self.preparing = False
        self.power = self.power_default

    def move(self):
        """
        Реакция пушки на изменение кадра.
        """
        self.y = min(max(0, self.y + self.vy), self.screen.get_clip().h)

        if self.preparing and self.power < self.power_max:
            self.power += self.power_increase

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
        v = 100
        x, y = self.ball_xy()
        ball = Ball(
            self.screen,
            x,
            y,
            20,
            v * self.power * math.cos(self.angle) * self.sgn,
            v * self.power * math.sin(self.angle),
            self.team,
            self.ball_color,
        )
        self.release()
        return ball

    def ball_xy(self):
        lever = self.w - self.r1
        return (
            self.x + (self.r1 / 2 + lever * math.cos(self.angle)) * self.sgn,
            self.y + lever * math.sin(self.angle),
        )

    def update_speed(self, direction):
        """Обновляет скорость движения пушки"""
        v = 10
        self.vy = v * direction

    def update_angle(self, pos):
        """Обновляет угол направления пушки."""
        x, y = pos
        x_rel = x - self.x - self.sgn * self.r1 / 2
        if x_rel < 0:
            return
        self.angle = math.atan2(y - self.y, x_rel)

    def draw(self):
        """Рисует пушку на экране."""

        barrel = pygame.Surface((self.w, self.r1))
        barrel.set_colorkey((0, 0, 0))
        p = (self.power - self.power_default) / \
            (self.power_max - self.power_default) * 0.3
        pygame.draw.polygon(barrel, self.barrel_color, [
            (self.r1 / 2, 0),
            (self.r1 / 2, self.r1),
            (self.w * (1 - p), (self.r1 + self.r2) / 2),
            (self.w * (1 - p), (self.r1 - self.r2) / 2),
        ])
        barrel_rotated = pygame.Surface((2 * self.w, 2 * self.w))
        barrel_rotated.set_colorkey((0, 0, 0))
        draw_rotated(
            barrel_rotated,
            self.r1 / 2,
            self.w,
            barrel,
            self.r1 / 2,
            self.r1 / 2,
            self.angle,
        )
        self.screen.blit(
            pygame.transform.flip(barrel_rotated, self.flipped, False),
            (self.x - (1 - self.sgn) * self.w, self.y - self.w),
        )

        r = self.r0
        base = pygame.Surface((r, 2*r))
        base.set_colorkey((0, 0, 0))
        pygame.draw.circle(base, self.body_color, (0, r), r)
        self.screen.blit(
            pygame.transform.flip(base, self.flipped, False),
            (self.x - (1 - self.sgn) * r / 2, self.y - r),
        )


class PlayerCannon(Cannon):
    def __init__(self, screen):
        super().__init__(screen, 0, screen.get_clip().h / 2, 0, 1, BLUE_COLORS)

    def draw(self):
        
        x0, y0 = self.ball_xy()
        w, h = self.screen.get_clip().size
        v = 100
        vx = v * self.power * math.cos(self.angle) * self.sgn
        vy = v * self.power * math.sin(self.angle)
        while 0 < x0 < w and 0 < y0 < h:
            v = 100
            x = x0 + vx
            y = y0 + vy 
            pygame.draw.aaline(self.screen, GREY, (x0, y0), ((x0 + x) / 2, (y0 + y) / 2))
            vy += 0.5
            x0 = x
            y0 = y

        super().draw()

    def update(self, event) -> Union[Ball, None]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.prepare()
        elif event.type == pygame.MOUSEBUTTONUP:
            return self.fire()
        elif event.type == pygame.MOUSEMOTION:
            self.update_angle(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.update_speed(-1)
            elif event.key == pygame.K_s:
                self.update_speed(+1)
        elif event.type == pygame.KEYUP:
            self.update_speed(0)
        return None


class ComputerCannon(Cannon):
    def __init__(self, screen):
        clip = screen.get_clip()
        super().__init__(screen, clip.w, clip.h // 2, 1, -1, RED_COLORS)

        self.angle_speed = math.pi / 48

        self.preparing_frames = 25
        self.frames = 0

        self.target_y = self.y

        self.prepare()

    def update(self) -> Union[Ball, None]:
        self.angle += self.angle_speed
        if self.angle >= math.pi / 2:
            self.angle = math.pi / 2 - 0.001
            self.angle_speed *= -1
        elif self.angle <= -math.pi / 2:
            self.angle = -math.pi / 2
            self.angle_speed *= -1

        ball = None
        if self.frames > self.preparing_frames:
            self.frames = 0
            ball = self.fire()
            self.prepare()

        while self.target_y - 10 <= self.y <= self.target_y + 10:
            self.target_y = randint(0, self.screen.get_clip().h)
            if self.target_y < self.y:
                self.update_speed(-1)
            else:
                self.update_speed(+1)

        self.frames += 1
        return ball
