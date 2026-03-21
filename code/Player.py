import pygame
from code.const import WIDTH, HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH


class Player:
    def __init__(self, x, ground_y):
        # ===== ANIMAÇÃO DO CORPO =====
        self.walk_frames_right = [
            pygame.image.load("asset/Walk_000.png").convert_alpha(),
            pygame.image.load("asset/Walk_001.png").convert_alpha(),
            pygame.image.load("asset/Walk_002.png").convert_alpha(),
            pygame.image.load("asset/Walk_003.png").convert_alpha(),
            pygame.image.load("asset/Walk_004.png").convert_alpha(),
            pygame.image.load("asset/Walk_005.png").convert_alpha(),
            pygame.image.load("asset/Walk_006.png").convert_alpha(),
            pygame.image.load("asset/Walk_007.png").convert_alpha(),
        ]

        # escala do corpo
        self.walk_frames_right = [
            pygame.transform.scale(img, (120, 220))
            for img in self.walk_frames_right
        ]

        # versão virada
        self.walk_frames_left = [
            pygame.transform.flip(img, True, False)
            for img in self.walk_frames_right
        ]

        # ===== ARMA =====
        self.weapon_right = pygame.image.load("asset/arm.png").convert_alpha()
        self.weapon_right = pygame.transform.scale(self.weapon_right, (95, 38))
        self.weapon_left = pygame.transform.flip(self.weapon_right, True, False)

        # ===== ESTADO =====
        self.direction = "right"
        self.frame_index = 0
        self.animation_speed = 0.18

        self.image = self.walk_frames_right[0]
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.ground_y = ground_y

        self.last_shot = 0
        self.shoot_delay = 200

        self.gun_sound = pygame.mixer.Sound("asset/gun_shot.wav")
        self.gun_sound.set_volume(0.5)

        self.move_x = 0
        self.move_y = 0
        self.is_moving = False

    # ===== MOVIMENTO =====
    def move(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        self.rect.x += dx
        self.rect.y += dy

        # limites
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 120:
            self.rect.top = 120
        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y

        self.move_x = dx
        self.move_y = dy
        self.is_moving = dx != 0 or dy != 0

    # ===== DIREÇÃO PELO MOUSE =====
    def update_direction(self):
        mouse_x, _ = pygame.mouse.get_pos()

        if mouse_x >= self.rect.centerx:
            self.direction = "right"
        else:
            self.direction = "left"

    # ===== ANIMAÇÃO =====
    def animate(self):
        bottom = self.rect.bottom
        centerx = self.rect.centerx

        if self.is_moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_frames_right):
                self.frame_index = 0

            if self.direction == "right":
                self.image = self.walk_frames_right[int(self.frame_index)]
            else:
                self.image = self.walk_frames_left[int(self.frame_index)]
        else:
            if self.direction == "right":
                self.image = self.walk_frames_right[0]
            else:
                self.image = self.walk_frames_left[0]

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom

    # ===== UPDATE =====
    def update(self, keys):
        self.move(keys)
        self.update_direction()
        self.animate()

    # ===== TIRO =====
    def can_shoot(self):
        now = pygame.time.get_ticks()
        return now - self.last_shot >= self.shoot_delay

    def shoot(self):
        self.last_shot = pygame.time.get_ticks()
        self.gun_sound.play()

    # ===== POSIÇÃO DA ARMA =====
    def get_gun_position(self):
        if self.direction == "right":
            return self.rect.centerx + 35, self.rect.centery - 28
        else:
            return self.rect.centerx - 35, self.rect.centery - 28

    # ===== ONDE A BALA NASCE =====
    def get_bullet_spawn(self):
        if self.direction == "right":
            bullet_x = self.rect.centerx + 102
            bullet_y = self.rect.centery + 20
        else:
            bullet_x = self.rect.centerx - 102
            bullet_y = self.rect.centery + 20

        return bullet_x, bullet_y

    # ===== DESENHO =====
    def draw(self, window):
        # corpo
        window.blit(self.image, self.rect)

        # arma por cima
        if self.direction == "right":
            weapon = self.weapon_right
            weapon_rect = weapon.get_rect(center=(self.rect.centerx + 35, self.rect.centery + 20))
        else:
            weapon = self.weapon_left
            weapon_rect = weapon.get_rect(center=(self.rect.centerx - 35, self.rect.centery + 20))

        window.blit(weapon, weapon_rect)