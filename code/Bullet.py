import pygame
import math
from code.const import WIDTH, HEIGHT, BULLET_SPEED


class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.radius = 5
        self.color = (255, 180, 0)

        self.x = x
        self.y = y

        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * BULLET_SPEED
        self.dy = math.sin(angle) * BULLET_SPEED

        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.alive = True

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.alive = False

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)