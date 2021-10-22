import math
from random import choice
from random import randint as rnd

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.g = 1
        self.save_k = 0.5
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.vy += self.g
        self.y += self.vy
        if self.screen.get_clip().h - self.r < self.y:
            self.y = self.screen.get_clip().h - self.r
            self.vx *= self.save_k
            self.vy *= -self.save_k

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (round(self.x), round(self.y)), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return obj.dist_from((self.x, self.y)) - self.r < 0


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY

        self.x = 40
        self.y = self.screen.get_clip().h / 2
        self.w = 100
        self.h = 40

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r = 15
        self.angle = math.atan2(event.pos[1] - self.y, event.pos[0] - self.x)
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan2(event.pos[1] - self.y, event.pos[0] - self.x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        sf = pygame.Surface((self.w, self.h))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.rect(sf, self.color, (0, 0, self.w, self.h))
        rotated = pygame.transform.rotate(sf, -self.angle * 180 / math.pi)
        beta = self.angle + math.pi / 4
        l = self.h / math.sqrt(2)
        self.screen.blit(rotated, (self.x, self.y))
        # self.screen.blit(rotated, (self.x + l * math.cos(beta), self.y - l * math.sin(beta)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.angle = 30
        self.w = 100
        self.h = 10
        self.color = RED
        self.screen = screen

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        sf = pygame.Surface((self.w, self.h))
        sf.set_colorkey((0, 0, 0))
        pygame.draw.rect(sf, self.color, (0, 0, self.w, self.h))
        rotated = pygame.transform.rotate(sf, -self.angle)
        self.screen.blit(rotated, (self.x, self.y))
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), 5)

    def dist_from(self, p):
        return 10000000000000000


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
bullet = 0
balls = []

clock = pygame.time.Clock()

screen_clip = screen.get_clip()
flipped_screen = pygame.Surface((screen_clip.w, screen_clip.h))
flipped_screen.set_colorkey((0, 0, 0))

gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target = Target()
    gun.power_up()

pygame.quit()
