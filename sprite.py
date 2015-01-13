from utils import Util
import math
import pygame
from pygame.locals import *

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
  IMG_CENTER = [64, 64]
  IMG_SIZE = [128, 128]

  def __init__(self, pos, canvas):
    Sprite.__init__(self, pos, [0, 0], 0, [0, 0], Explosion.RADIUS, canvas)
    self.img = Image.open('./images/explosion_alpha.png')
    self.age = 0
    self.x = self.pos[0] - Explosion.IMG_CENTER[0]
    self.y = self.pos[1] - Explosion.IMG_CENTER[1]
    self.sound = False

  def draw(self):
    if self.sound == False:
      sound.explosion.play()
      self.sound = True

    x1 = 0 + self.age * Explosion.IMG_SIZE[0]
    y1 = 0
    x2 = x1 + Explosion.IMG_SIZE[0]
    y2 = Explosion.IMG_SIZE[1]
    image = self.img.crop((x1, y1, x2, y2))
    self.image = ImageTk.PhotoImage(image)
    self.canvas.create_image(self.x, self.y, anchor=Tkinter.NW, image=self.image)

  def update(self):
    # update age
    self.age += 1
    if self.age > Bullet.LIFE:
        return True

    return False