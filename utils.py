import pygame
import math


def draw_rotated(dst, x, y, src, ox, oy, angle):
    """
    Рисует объект pygame.Surface, повёрнутый на данный угол относительно данной точки на ней.
    Угол задаётся в радианах от -math.pi/2 до math.pi/2.
    """
    lever = math.sqrt(ox ** 2 + oy ** 2)
    clip = src.get_clip()
    if angle > 0:
        beta = angle + math.atan2(oy, ox)
        dx = -lever * math.cos(beta) - clip.h * math.sin(angle)
        dy = -lever * math.sin(beta)
    else:
        beta = -angle + math.atan2(ox, oy)
        dx = -lever * math.sin(beta)
        dy = -lever * math.cos(beta) + clip.w * math.sin(angle)
    rotated = pygame.transform.rotate(src, -angle * 180 / math.pi)
    dst.blit(rotated, (x + dx, y + dy))
