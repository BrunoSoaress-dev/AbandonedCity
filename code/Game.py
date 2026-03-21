import pygame
import sys

from code.Menu import Menu
from code.Level import Level
from code.const import WIDTH, HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Abandoned City")

        self.scores = []  # lista de scores

    def run(self):
        while True:
            menu = Menu(self.window, self.scores)
            action = menu.run()

            if action == "NEW GAME":
                level = Level(self.window)
                result, score = level.run()

                # salva score
                self.scores.append(score)
                self.scores = sorted(self.scores, reverse=True)[:10]

            elif action == "SCORE":
                menu.show_scores()