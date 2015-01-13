from utils import Util
import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Ship(pygame.sprite.Sprite):
  """moves a clenched fist on the screen, following the mouse"""
  def __init__(self, pos, vel, angle):
    pygame.sprite.Sprite.__init__(self)
    self.image1, self.rect1 = Util.load_image('ship_unspeed.png')
    self.image2, self.rect2 = Util.load_image('ship_speed.png')
    self.image, self.rect = self.image1, self.rect1
    self.original1 = self.image1
    self.original2 = self.image2
    self.rect.move_ip(pos)
    self.rect.move_ip([-self.rect.width / 2, -self.rect.height / 2])

    self.vel = vel
    self.angle = angle
    self.angle_vel = 0
    self.thrust = False
    self.game_on = False
    self.radius = 35
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()

  def update(self):
    # change image
    if self.thrust == False:
      self.image = self.image1
      self.original = self.image1
    else:
      self.image = self.image2
      self.original = self.image2

    # update angle
    self.angle += self.angle_vel
    self.angle %= 360

    # update position
    # move by move_ip will move by upleft coord,
    # but it is not good
    # TODO: there are some bugs about rect.move, 
    # the move is not smooth, make it smooth
    self.rect.move_ip(self.vel)

    # make ship in screen
    if self.rect.right < self.area.left:
      self.rect.move_ip([self.area.width, 0])
    elif self.rect.left > self.area.right:
      self.rect.move_ip([-self.area.width, 0])
    elif self.rect.bottom < self.area.top:
      self.rect.move_ip([0, self.area.height])
    elif self.rect.top > self.area.bottom:
      self.rect.move_ip([0, -self.area.height])

    # rotate,  not smooth, bad for pygame
    center = self.rect.center
    rotate = pygame.transform.rotate
    self.image = rotate(self.original, self.angle)
    self.rect = self.image.get_rect(center=center)

    # update velocity
    if self.thrust == True:
      acc = Util.angle_to_vector(self.angle)
      self.vel[0] += acc[0] * .2
      self.vel[1] -= acc[1] * .2

    self.vel[0] *= .99
    self.vel[1] *= .99

    if self.game_on == False:
      self.angle_vel *= 0.98

  def set_thrust(self, status):
    self.thrust = status

  def increment_angle_vel(self):
    self.angle_vel += 2

  def decrement_angle_vel(self):
    self.angle_vel -= 2

  def reset_angle_vel(self):
    self.angle_vel = 0.0

  def set_game_status(self, status):
    self.game_on = status

  def shoot(self):
    forward = Util.angle_to_vector(self.angle)
    missile_pos = [self.rect.center[0] + self.radius * forward[0], self.rect.center[1] - self.radius * forward[1]]
    missile_speed = [15 * forward[0], -15 * forward[1]]
    missile_vel = [self.vel[0] + missile_speed[0], self.vel[1] + missile_speed[1]]
    a_missile = Missile(missile_pos, missile_vel)
    return a_missile

class Missile(pygame.sprite.Sprite):
  LIFE = 25

  def __init__(self, pos, vel):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Util.load_image('shot2.png')
    self.rect.move_ip(pos)
    self.rect.move_ip([-self.rect.width / 2, -self.rect.height / 2])
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.pos = pos
    self.vel = vel
    self.age = 0

  def update(self):
    # update position
    self.age += 1
    if self.age > Missile.LIFE:
        return True

    self.rect.move_ip(self.vel)
    # make missile in screen
    if self.rect.right < self.area.left:
      self.rect.move_ip([self.area.width, 0])
    elif self.rect.left > self.area.right:
      self.rect.move_ip([-self.area.width, 0])
    elif self.rect.bottom < self.area.top:
      self.rect.move_ip([0, self.area.height])
    elif self.rect.top > self.area.bottom:
      self.rect.move_ip([0, -self.area.height])

    return False