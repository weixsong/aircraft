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
    self.rect.move_ip([-self.rect.width / 2, -self.rect.height / 2]) # move the ship to center
    self.original1 = self.image1
    self.original2 = self.image2
    self.rect.move_ip(pos)

    self.vel = vel
    self.angle = angle
    self.angle_vel = 0
    self.game_on = False
    self.thrust = False
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()

  def update(self):
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
    self.rect.move_ip(self.vel)
    if self.rect.right < self.area.left:
      self.rect.move_ip([self.area.width, 0])
    elif self.rect.left > self.area.right:
      self.rect.move_ip([-self.area.width, 0])
    elif self.rect.bottom < self.area.top:
      self.rect.move_ip([0, self.area.height])
    elif self.rect.top > self.area.bottom:
      self.rect.move_ip([0, -self.area.height])

    # rotate
    self.image = Util.rot_center(self.original, self.angle)

    # update velocity
    if self.thrust == True:
      acc = Util.angle_to_vector(-self.angle)
      self.vel[0] += acc[0] * .2
      self.vel[1] += acc[1] * .2

    self.vel[0] *= .99
    self.vel[1] *= .99

    if self.game_on == False:
      self.angle_vel *= 0.98

  def increment_angle_vel(self):
    self.angle_vel -= 0.03

  def decrement_angle_vel(self):
    self.angle_vel += 0.03

  def reset_angle_vel(self):
    self.angle_vel = 0.0

  def set_game_state(self, state):
    self.game_on = state

  def shoot(self, missile_group):
    #TODO: fix this
    pass
    forward = Util.angle_to_vector(self.angle)
    radius = self.get_radius()
    missile_pos = [self.pos[0] + radius * forward[0], self.pos[1] - radius * forward[1]]
    missile_vel = [self.vel[0] + 15 * forward[0], self.vel[1] + 15 * forward[1]]
    a_missile = Bullet(missile_pos, missile_vel, self.angle, 0, self.canvas)
    missile_group.add(a_missile)