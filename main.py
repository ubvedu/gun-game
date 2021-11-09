import pygame
from gun import Gun
from target import Target
from colors import WHITE, BLACK

FPS = 30

WIDTH = 800
HEIGHT = 600

pygame.init()
pygame.display.set_caption('Rainbow come machine')
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
bullets = 0
balls = []

clock = pygame.time.Clock()

gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    for b in balls:
        b.draw()
    gun.draw()
    target.draw()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.prepare()
        elif event.type == pygame.MOUSEBUTTONUP:
            ball = gun.fire()
            bullets += 1
            balls.append(ball)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.collide(target):
            target.hit()
            target = Target(screen)
    gun.power_up()
    pygame.display.update()

pygame.quit()
