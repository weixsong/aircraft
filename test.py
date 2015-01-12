from utils import Util
import pygame

pygame.init()
screen = pygame.display.set_mode((468, 60))
img, rect = Util.load_image('double_ship.png')
print rect
