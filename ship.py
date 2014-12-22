import Image 
import ImageTk
from utils import Util
import Tkinter
import pygame
import time
import math

class Ship:
  def __init__(self, pos, vel, angle, canvas):
    self.pos = [pos[0], pos[1]]
    self.vel = [vel[0], vel[1]]
    self.thrust = False

    self.angle = angle
    self.angle_vel = 0

    self.image_radius = 35
    self.image_center = [45, 45]
    self.image_size = [90, 90]
    self.canvas = canvas
    img = Image.open("./images/double_ship.png")
    self.image_unthrust = img.crop((0, 0, self.image_size[0] - 1, self.image_size[1] - 1))
    self.image_thrust = img.crop((self.image_size[0], 0, self.image_size[0] + self.image_size[0] - 1, self.image_size[1]))

    pygame.mixer.init()
    self.sound = pygame.mixer.music.load("./sounds/thrust.mp3")

  def draw(self):
    upleft_x = self.pos[0] - self.image_center[0]
    upleft_y = self.pos[1] - self.image_center[1]
    if self.thrust:
      self.img = ImageTk.PhotoImage(self.image_thrust.rotate(self.angle * 180 / math.pi, resample=Image.BICUBIC))
      # self.img = ImageTk.PhotoImage(self.image_thrust)
      self.canvas.create_image(upleft_x, upleft_y, anchor=Tkinter.NW, image=self.img)
    else:
      self.img = ImageTk.PhotoImage(self.image_unthrust.rotate(self.angle * 180 / math.pi, resample=Image.BICUBIC))
      # self.img = ImageTk.PhotoImage(self.image_unthrust)
      self.canvas.create_image(upleft_x, upleft_y, anchor=Tkinter.NW, image=self.img)

  def update(self):
    # update angle
    self.angle += self.angle_vel

    # update position
    self.pos[0] = (self.pos[0] + self.vel[0]) % self.canvas.CANVAS_WIDTH
    self.pos[1] = (self.pos[1] - self.vel[1]) % self.canvas.CANVAS_HEIGHT

    # update velocity
    if self.thrust:
      acc = Util.angle_to_vector(self.angle)
      self.vel[0] += acc[0] * .1
      self.vel[1] += acc[1] * .1

    self.vel[0] *= .99
    self.vel[1] *= .99

  def set_thrust(self, on):
    # TODO: how to play mp3?
    self.thrust = on
    if on:
      pygame.mixer.music.play()
    else:
      pygame.mixer.music.stop()

  def increment_angle_vel(self):
    self.angle_vel += 0.03

  def decrement_angle_vel(self):
    self.angle_vel -= 0.03

  def get_position(self):
    return self.pos
    
  def get_radius(self):
    return self.radius

  def shoot(self, missile_group):
    # TODO: fix this
    forward = angle_to_vector(self.angle)
    missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
    missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
    a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
    missile_group.add(a_missile)