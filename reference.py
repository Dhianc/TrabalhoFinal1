import sys
import random
import pygame
from pygame.locals import *
from control import Simulation
import numpy as np
from os import path

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

images_path = 'images'
bg_image = pygame.image.load(path.join(images_path, 'ceu.jpg'))


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Pygame Drone')
screen.blit(bg_image, (0, 0))


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, scale):
        super().__init__()

        # self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # pygame.draw.polygon(self.image, (0, 0, 0), ((0, 0), (width, 0), (width, height), (0, height)))
        img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.original_image = self.image

        self.rect = self.image.get_rect(center = (0, 0))

    def update(self, pos_x, pos_y, angle):
        self.rect.move_ip(pos_x, pos_y)

        self.image = pygame.transform.rotate(self.original_image, angle * 180 / np.pi)
        self.rect = self.image.get_rect(center = self.rect.center)

    def draw(self):
        screen.blit(self.image, self.rect)


P = Player(f'images/drone/drone6.png', 50, 5, 0.2)
S = Simulation()

pos_last_px = np.array([0, 0])

def interpolate(xa, x1, x2, y1, y2):
    return ((xa - x1) / (x2 - x1) * (y2 - y1)) + y1


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not S.is_over():
        pos_abs_m, angle = S.iterate()

        x_abs_px = interpolate(pos_abs_m[0], -60, 25, 0, SCREEN_WIDTH)
        y_abs_px = interpolate(pos_abs_m[1], -2, 17, 0, SCREEN_HEIGHT)
        y_abs_px = SCREEN_HEIGHT - y_abs_px

        pos_abs_px = np.array([int(x_abs_px), int(y_abs_px)])
        pos_rel_px = pos_abs_px - pos_last_px
        pos_last_px = pos_abs_px

        P.update(pos_rel_px[0], pos_rel_px[1], angle)
    else:
        pygame.quit()
        sys.exit()

    screen.blit(bg_image, (0, 0))
    P.draw()

    pygame.display.update()
    clock.tick(1000)