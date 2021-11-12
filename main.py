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
targets = [Target(screen) for _ in range(5)]
finished = False

while not finished:
    screen.fill(WHITE)
    for b in balls:
        b.draw()
    gun.draw()
    for t in targets:
        t.draw()

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
            gun.target(event)

    for b in balls:
        b.move()
        for t in targets:
            if b.collide(t):
                target.hit()
                target = Target(screen)
    for t in targets:
        t.move()
    balls = list(filter(lambda b: not b.is_out(), balls))
    gun.power_up()
    pygame.display.update()

pygame.quit()
