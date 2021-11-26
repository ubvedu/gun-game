import pygame
from cannon import Cannon
from spinner import SpinnerSpawner
from gate import Gate
from colors import WHITE, GREEN

FPS = 30

WIDTH = 800
HEIGHT = 600

pygame.init()
pygame.display.set_caption('Pinball cannons')
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
bullets = 0
balls = []

clock = pygame.time.Clock()

gun = Cannon(screen)
target_spawner = SpinnerSpawner(screen)
finished = False

clip = screen.get_clip()
gate = Gate(screen, clip.w // 2, 2*clip.w, GREEN)

def check(ball):
    if ball.is_out():
        gate.check(ball.x)
        return False
    return True

font32 = pygame.font.SysFont(None, 32)
def draw_score(score):
    sf = font32.render(str(score), True, GREEN)
    screen.blit(sf, (32, 32))


while not finished:
    screen.fill(WHITE)
    for b in balls:
        b.draw()
    gun.draw()
    target_spawner.draw()
    gate.draw()
    draw_score(gate.goals)
    

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                gun.vy = -5
            elif event.key == pygame.K_s:
                gun.vy = 5
        elif event.type == pygame.KEYUP:
            gun.vy = 0

    gun.move()
    for b in balls:
        b.move()
        b.collide(target_spawner)
    target_spawner.move()
    balls = list(filter(check, balls))
    gun.power_up()
    pygame.display.update()

pygame.quit()
