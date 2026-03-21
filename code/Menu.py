import pygame
import sys
from code.const import WIDTH, HEIGHT, ORANGE, BLACK


class Menu:
    def __init__(self, window, scores):
        self.window = window
        self.selected_option = 0
        self.options = ["NEW GAME", "SCORE", "EXIT", "CONTROLS"]

        self.scores = scores

        self.title_font = pygame.font.SysFont("arial", 52, bold=True)
        self.option_font = pygame.font.SysFont("arial", 32, bold=True)
        self.small_font = pygame.font.SysFont("arial", 24)

        self.background = pygame.image.load("asset/menu_background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        pygame.mixer.music.load("asset/menu_sound.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # ================= MENU PRINCIPAL =================
    def draw(self):
        self.window.blit(self.background, (0, 0))

        title = self.title_font.render("ABANDONED CITY", True, ORANGE)
        self.window.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        for i, option in enumerate(self.options):
            color = ORANGE if i == self.selected_option else BLACK
            text = self.option_font.render(option, True, color)
            self.window.blit(text, text.get_rect(center=(WIDTH // 2, 220 + i * 55)))

        pygame.display.flip()

    # ================= CONTROLS =================
    def controls_screen(self):
        while True:
            self.window.blit(self.background, (0, 0))

            title = self.title_font.render("CONTROLS", True, ORANGE)
            self.window.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

            controls = [
                "W - Move Up",
                "S - Move Down",
                "A - Move Left",
                "D - Move Right",
                "Mouse - Aim",
                "Left Click - Shoot",
                "ESC - Pause / Back",
                "R - Restart Game",
                "UP / DOWN - Menu Navigation",
                "ENTER - Select Option"
            ]

            for i, line in enumerate(controls):
                text = self.small_font.render(line, True, BLACK)
                self.window.blit(text, text.get_rect(center=(WIDTH // 2, 180 + i * 30)))

            back = self.small_font.render("Press ESC to return", True, ORANGE)
            self.window.blit(back, back.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    # ================= SCORE =================
    def show_scores(self):
        while True:
            self.window.blit(self.background, (0, 0))

            title = self.title_font.render("SCORES", True, ORANGE)
            self.window.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

            if len(self.scores) == 0:
                text = self.small_font.render("No scores yet", True, BLACK)
                self.window.blit(text, text.get_rect(center=(WIDTH // 2, 200)))
            else:
                for i, score in enumerate(self.scores):
                    score_text = self.small_font.render(
                        f"{i + 1}. {score}", True, BLACK
                    )
                    self.window.blit(score_text, (WIDTH // 2 - 50, 180 + i * 30))

            back = self.small_font.render("Press ESC to return", True, ORANGE)
            self.window.blit(back, back.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    # ================= LOOP DO MENU =================
    def run(self):
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)

                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        selected = self.options[self.selected_option]

                        if selected == "NEW GAME":
                            pygame.mixer.music.stop()
                            return "NEW GAME"

                        elif selected == "SCORE":
                            return "SCORE"

                        elif selected == "EXIT":
                            pygame.quit()
                            sys.exit()

                        elif selected == "CONTROLS":
                            self.controls_screen()