import math
import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Util:
  INIT_MIXER = False
  INIT_DISPLAY = False

  @staticmethod
  def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

  @staticmethod
  def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

  @staticmethod
  def load_image(name, colorkey=None):
    if Util.INIT_DISPLAY == False:
      pygame.display.init()
      Util.INIT_DISPLAY = True

    fullname = os.path.join('./images/', name)
    try:
      image = pygame.image.load(fullname)
    except pygame.error, message:
      print 'Cannot load image:', name
      raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
      if colorkey is -1:
        colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

  @staticmethod
  def load_sound(name):
    class NoneSound:
      def play(self):
        pass

    if Util.INIT_MIXER == False:
      pygame.mixer.init()
      Util.INIT_MIXER = True

    if not pygame.mixer:
      return NoneSound()
    fullname = os.path.join('./sounds/', name)
    try:
      sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
      print 'Cannot load sound:', wav
      raise SystemExit, message
    return sound
