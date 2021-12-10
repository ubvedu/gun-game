import pygame
from ball import Ball
from cannon import Cannon, ComputerCannon, PlayerCannon
from spinner import SpinnerSpawner
from gate import Gate
from colors import WHITE, GREEN, BLUE_COLORS, RED_COLORS
from wall import Wall

FPS = 30

WIDTH = 1280
HEIGHT = 720

pygame.init()
pygame.display.set_caption('Pinball cannons')
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clip = screen.get_clip()
balls = list[Ball]()

clock = pygame.time.Clock()

cannon1 = PlayerCannon(screen)
cannon2 = ComputerCannon(screen)
target_spawner = SpinnerSpawner(screen)
wall1 = Wall(0)
wall2 = Wall(clip.w)


finished = False

gate1 = Gate(screen, 0, clip.w // 2, 0, BLUE_COLORS[2])
gate2 = Gate(screen, clip.w // 2 + 1, clip.w, 1, RED_COLORS[2])


def check(ball):
    if ball.is_out():
        gate1.check(ball)
        gate2.check(ball)
        return False
    return True


font32 = pygame.font.SysFont(None, 32)


def draw_score(score, x, y, color):
    sf = font32.render(str(score), True, color)
    clip = sf.get_clip()
    screen.blit(sf, (x - clip.w / 2, y - clip.h / 2))


while not finished:
    screen.fill(WHITE)
    for b in balls:
        b.draw()
    cannon1.draw()
    cannon2.draw()
    target_spawner.draw()
    gate1.draw()
    gate2.draw()
    draw_score(gate2.goals, clip.w // 2 - 32, clip.h - 32, BLUE_COLORS[2])
    draw_score(gate1.goals, clip.w // 2 + 32, clip.h - 32, RED_COLORS[2])

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            ball = cannon1.update(event)
            if ball is not None:
                balls.append(ball)

    ball = cannon2.update()
    if ball is not None:
        balls.append(ball)

    cannon1.move()
    cannon2.move()
    for b in balls:
        b.move()
        b.collide(target_spawner)
        b.collide(wall1)
        b.collide(wall2)
    target_spawner.move()
    balls = list(filter(check, balls))
    pygame.display.update()

pygame.quit()
