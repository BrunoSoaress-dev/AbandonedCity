import pygame
import sys
import random

from code.Player import Player
from code.Enemy import Enemy
from code.Bullet import Bullet
from code.Background import Background
from code.const import WIDTH, HEIGHT, FPS, WHITE, RED


class Level:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()

        self.background = Background()

        self.ground_y = HEIGHT - 35
        self.player = Player(WIDTH // 2, self.ground_y)

        self.enemies = []
        self.bullets = []

        self.spawn_timer = 0
        self.score = 0

        pygame.mixer.music.load("asset/game_ambience.wav")
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.big_font = pygame.font.SysFont("arial", 52, bold=True)

    def spawn_enemy(self):
        side = random.choice(["left", "right"])

        if side == "left":
            x = -60
        else:
            x = WIDTH + 60

        self.enemies.append(Enemy(x, self.ground_y))

    def draw_ui(self):
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)

        self.window.blit(health_text, (20, 20))
        self.window.blit(score_text, (20, 55))

    def game_over_screen(self):
        while True:
            self.window.fill((20, 20, 20))

            title = self.big_font.render("GAME OVER", True, RED)
            score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            info = self.font.render("Press R to return menu", True, WHITE)

            self.window.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            self.window.blit(score, score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
            self.window.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        return "MENU"

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return "MENU"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.player.can_shoot():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.player.shoot()

                        bullet_x, bullet_y = self.player.get_bullet_spawn()

                        self.bullets.append(
                            Bullet(bullet_x, bullet_y, mouse_x, mouse_y)
                        )

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.background.update(self.player.move_x)

            self.spawn_timer += 1
            if self.spawn_timer >= 90:
                self.spawn_enemy()
                self.spawn_timer = 0

            for bullet in self.bullets:
                bullet.update()

            self.bullets = [b for b in self.bullets if b.alive]

            for enemy in self.enemies:
                enemy.update(self.player)
                enemy.attack(self.player)

            for bullet in self.bullets:
                for enemy in self.enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        bullet.alive = False
                        enemy.health -= 1

            alive_enemies = []
            for enemy in self.enemies:
                if enemy.health > 0:
                    alive_enemies.append(enemy)
                else:
                    self.score += 10
            self.enemies = alive_enemies

            self.bullets = [b for b in self.bullets if b.alive]

            self.background.draw(self.window)

            for bullet in self.bullets:
                bullet.draw(self.window)

            self.player.draw(self.window)

            for enemy in self.enemies:
                enemy.draw(self.window)

            self.draw_ui()
            pygame.display.flip()

            if self.player.health <= 0:
                result = self.game_over_screen()
                return result, self.score