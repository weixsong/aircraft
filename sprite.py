from utils import Util
import math
import pygame
from pygame.locals import *
import sound

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Rock(pygame.sprite.Sprite):
  LIMIT = 12
  RADIUS = 40

  def __init__(self, pos, vel, angle_vel):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Util.load_image('asteroid_blue.png')
    self.original = self.image
    self.area = pygame.display.get_surface().get_rect()
    self.vel = vel
    self.angle_vel = angle_vel
    self.angle = 0

    self.rect.move_ip(pos)
    self.rect.move_ip([-self.rect.width / 2, -self.rect.height / 2])

  def update(self):
    # update angle
    self.angle += self.angle_vel

    # update position
    self.rect.move_ip(self.vel)
    # rotate,  not smooth, bad for pygame
    center = self.rect.center
    rotate = pygame.transform.rotate
    self.image = rotate(self.original, self.angle)
    self.rect = self.image.get_rect(center=center)

    # make rock in screen
    if self.rect.right < self.area.left:
      self.rect.move_ip([self.area.width, 0])
    elif self.rect.left > self.area.right:
      self.rect.move_ip([-self.area.width, 0])
    elif self.rect.bottom < self.area.top:
      self.rect.move_ip([0, self.area.height])
    elif self.rect.top > self.area.bottom:
      self.rect.move_ip([0, -self.area.height])

class Explosion(pygame.sprite.Sprite):
  RADIUS = 17
  LIFE = 24

  def __init__(self, pos):
    pygame.sprite.Sprite.__init__(self)
    self.original, self.rect = Util.load_image('explosion_alpha.png')
    self.rect = pygame.Rect(pos[0] - 64, pos[1] - 64, 128, 128)
    self.pos = pos
    self.height = self.rect.height
    r = pygame.Rect(0, 0, self.height, self.height)
    self.image = self.original.subsurface(r)
    self.age = 0
    sound.explosion.play()

  def update(self):
    # update age
    self.age += 1
    if self.age >= Explosion.LIFE:
        return True
    r = pygame.Rect(self.age * self.height, 0, self.height, self.height)
    self.image = self.original.subsurface(r)
    return False