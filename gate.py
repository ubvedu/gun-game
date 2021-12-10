import pygame

class Gate:
    def __init__(self, screen, a, b, team, color):
        self.screen = screen
        self.a = a
        self.b = b
        self.color = color
        self.team = team
        self.goals = 0

    def draw(self):
        sf = self.screen.convert_alpha()
        clip = sf.get_clip()
        n = 20
        for i, y in enumerate(range(clip.h, clip.h - 20, -1)):
            self.color.a = 255 - 255 * i // n
            pygame.draw.line(sf, self.color, (self.a, y), (self.b, y))
        self.screen.blit(sf, (0, 0))

    def check(self, ball):
        if self.a < ball.x < self.b and ball.team != self.team:
            self.goals += 1
