import pygame

class Gate:
    def __init__(self, screen, a, b, color):
        self.screen = screen
        self.a = a
        self.b = b
        self.color = color
        self.goals = 0

    def draw(self):
        sf = self.screen.convert_alpha()
        clip = sf.get_clip()
        a = max(self.a, 0)
        b = min(self.b, clip.w)
        n = 20
        for i, y in enumerate(range(clip.h, clip.h - 20, -1)):
            self.color.a = 255 - 255 * i // n
            pygame.draw.line(sf, self.color, (self.a, y), (self.b, y))
        self.screen.blit(sf, (0, 0))

    def check(self, x):
        if self.a < x < self.b:
            self.goals += 1
