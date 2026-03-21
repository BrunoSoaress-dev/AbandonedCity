import pygame
import math
from code.const import ENEMY_SPEED


class Enemy:
    def __init__(self, x, ground_y):
        self.frames_right = [
            pygame.image.load("asset/Walk1.png").convert_alpha(),
            pygame.image.load("asset/Walk2.png").convert_alpha(),
            pygame.image.load("asset/Walk3.png").convert_alpha(),
            pygame.image.load("asset/Walk4.png").convert_alpha(),
            pygame.image.load("asset/Walk5.png").convert_alpha(),
            pygame.image.load("asset/Walk6.png").convert_alpha(),
        ]

        # tamanho dos frames
        self.frames_right = [
            pygame.transform.scale(frame, (95, 150))
            for frame in self.frames_right
        ]

        # versões viradas para o outro lado
        self.frames_left = [
            pygame.transform.flip(frame, True, False)
            for frame in self.frames_right
        ]

        self.direction = "left"
        self.frame_index = 0
        self.animation_speed = 0.18

        self.image = self.frames_left[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

        self.speed = ENEMY_SPEED
        self.health = 3

        self.attack_cooldown = 800
        self.last_attack = 0

        self.sound = pygame.mixer.Sound("asset/zombie.wav")
        self.sound.set_volume(0.4)

        self.ground_y = ground_y

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames_right):
            self.frame_index = 0

        current_bottom = self.rect.bottom
        current_centerx = self.rect.centerx

        if self.direction == "right":
            self.image = self.frames_right[int(self.frame_index)]
        else:
            self.image = self.frames_left[int(self.frame_index)]

        self.rect = self.image.get_rect()
        self.rect.centerx = current_centerx
        self.rect.bottom = current_bottom

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.bottom - self.rect.bottom

        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # direção visual do zumbi
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"

        # manter no chão
        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y

        self.animate()

    def attack(self, player):
        now = pygame.time.get_ticks()

        if self.rect.colliderect(player.rect):
            if now - self.last_attack >= self.attack_cooldown:
                player.health -= 1
                self.last_attack = now
                self.sound.play()

    def draw(self, window):
        window.blit(self.image, self.rect)