import pygame
from code.const import WIDTH, HEIGHT


class Background:
    def __init__(self):
        self.layers = [
            {
                "image": pygame.image.load("asset/Back_pale.png").convert_alpha(),
                "speed": 0.10,
                "x": 0
            },
            {
                "image": pygame.image.load("asset/bg_layer_1.png").convert_alpha(),
                "speed": 0.20,
                "x": 0
            },
            {
                "image": pygame.image.load("asset/bg_layer_2.png").convert_alpha(),
                "speed": 0.35,
                "x": 0
            },
            {
                "image": pygame.image.load("asset/houses1_pale.png").convert_alpha(),
                "speed": 0.50,
                "x": 0
            },
            {
                "image": pygame.image.load("asset/bg_layer_3.png").convert_alpha(),
                "speed": 0.80,
                "x": 0
            },
            {
                "image": pygame.image.load("asset/bg_layer_4.png").convert_alpha(),
                "speed": 1.10,
                "x": 0
            },
        ]

        for layer in self.layers:
            layer["image"] = pygame.transform.scale(layer["image"], (WIDTH, HEIGHT))

    def update(self, move_x):
        for layer in self.layers:
            layer["x"] -= move_x * layer["speed"]

            if layer["x"] <= -WIDTH:
                layer["x"] += WIDTH
            elif layer["x"] >= WIDTH:
                layer["x"] -= WIDTH

    def draw(self, window):
        for layer in self.layers:
            x = layer["x"]
            image = layer["image"]

            window.blit(image, (x, 0))
            window.blit(image, (x + WIDTH, 0))
            window.blit(image, (x - WIDTH, 0))