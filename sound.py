import utils
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.mixer.init()
thrust = pygame.mixer.Sound("./sounds/thrust.ogg")
explosion = pygame.mixer.Sound("./sounds/explosion.ogg")
missile = pygame.mixer.Sound("./sounds/missile.ogg")
soundtrack = pygame.mixer.Sound("./sounds/soundtrack.ogg")
