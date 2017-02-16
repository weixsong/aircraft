from utils import Util
import math
import pygame
from pygame.locals import *
import sound

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class AircraftSprite(pygame.sprite.Sprite):
  def __init__(self, img_path, pos, vel, angle, angle_vel):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = Util.load_image(img_path)
    self.original = self.image
    # move this sprite to target position
    self.pos = pos
    self.vel = vel
    self.angle = angle
    self.angle_vel = angle_vel
    self.rect.move_ip(pos)
    self.rect.move_ip([-self.rect.width / 2, -self.rect.height / 2])

    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.rotate = pygame.transform.rotate

  def rotate_img(self):
    center = self.get_center()
    self.image = self.rotate(self.original, self.angle)
    self.rect = self.image.get_rect(center=center)

  def get_center(self):
    return self.rect.center

  def get_width(self):
    return self.rect.width

  def get_height(self):
    return self.rect.height

  def update(self):
    assert False, "action should be defined"

class Ship(AircraftSprite):
  def __init__(self, pos, vel, angle):
    AircraftSprite.__init__(self, 'ship_unspeed.png', pos, vel, angle, 0)
    self.image1, self.rect1 = Util.load_image('ship_unspeed.png')
    self.image2, self.rect2 = Util.load_image('ship_speed.png')
    self.original1 = self.image1
    self.original2 = self.image2

    self.thrust = False
    self.game_on = False
    self.radius = 35

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
    self.rotate_img()

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
    if status == True:
      sound.thrust.play()
    else:
      sound.thrust.stop()

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
    center = self.get_center()
    missile_pos = [center[0] + self.radius * forward[0], center[1] - self.radius * forward[1]]
    missile_speed = [15 * forward[0], -15 * forward[1]]
    missile_vel = [self.vel[0] + missile_speed[0], self.vel[1] + missile_speed[1]]
    a_missile = Missile(missile_pos, missile_vel)
    return a_missile

class Missile(AircraftSprite):
  LIFE = 25

  def __init__(self, pos, vel):
    AircraftSprite.__init__(self, 'shot2.png', pos, vel, 0, 0)
    self.age = 0
    sound.missile.play()

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

class Rock(AircraftSprite):
  LIMIT = 12
  RADIUS = 40

  def __init__(self, pos, vel, angle_vel):
    AircraftSprite.__init__(self, 'asteroid_blue.png', pos, vel, 0, angle_vel)

  def update(self):
    # update angle
    self.angle += self.angle_vel
    # update position
    self.rect.move_ip(self.vel)
    # rotate,  not smooth, bad for pygame
    self.rotate_img()
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