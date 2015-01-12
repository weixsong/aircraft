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
    self.image, self.rect = Util.load_image('double_ship.png')
    self.original = self.image
    self.rect.move_ip(pos)

    self.vel = vel
    self.angle = angle
    self.angle_vel = 0
    self.game_on = False
    self.thrust = False
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()

  def update(self):
    # update angle
    self.angle += self.angle_vel

    # update position
    self.rect.move_ip(self.vel)
    if self.rect.left < self.area.left or self.rect.right > self.area.right:
      self.vel[0] = -self.vel[0]
    if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
      self.vel[1] = -self.vel[1]

    # rotate
    rotate = pygame.transform.rotate
    self.image = rotate(self.original, self.angle)

    # update velocity
    if self.thrust == True:
      acc = Util.angle_to_vector(-self.angle)
      self.vel[0] += acc[0] * .2
      self.vel[1] += acc[1] * .2

    self.vel[0] *= .99
    self.vel[1] *= .99

    if self.game_on == False:
      self.angle_vel *= 0.99

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