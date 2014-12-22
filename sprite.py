import Image 
import ImageTk
import Tkinter
from utils import Util
import math

class Sprite:
  ''' base class for Rock, Bullet '''

  def __init__(self, pos, vel, ang, ang_vel, radius, canvas):
    self.pos = pos
    self.vel = vel
    self.angle = ang
    self.angle_vel = ang_vel
    self.radius = radius
    self.canvas = canvas

  def collide(self, other_object):
    distance = Util.dist(self.get_position(), other_object.get_position())
    sum_r = self.get_radius() + other_object.get_radius()
    if distance > sum_r:
      return False
    else:
      return True

  def draw(self):
    assert False, "action should be defined"

  def update(self):
    assert False, "action should be defined"

  def get_position(self):
    return self.pos

  def get_radius(self):
    return self.radius

class Rock(Sprite):
  LIMIT = 12
  RADIUS = 40
  IMG_CENTER = [45, 45]
  IMG_SIZE = [90, 90]

  def __init__(self, pos, vel, ang, ang_vel, canvas):
    Sprite.__init__(self, pos, vel, ang, ang_vel, Rock.RADIUS, canvas)
    self.img = Image.open("./images/asteroid_blue.png")

  def draw(self):
    upleft_x = self.pos[0] - Rock.IMG_CENTER[0]
    upleft_y = self.pos[1] - Rock.IMG_CENTER[1]
    self.image = ImageTk.PhotoImage(self.img.rotate(self.angle * 180 / math.pi, resample=Image.BICUBIC))
    self.canvas.create_image(upleft_x, upleft_y, anchor=Tkinter.NW, image=self.image)

  def update(self):
    # update angle
    self.angle += self.angle_vel

    # update position
    self.pos[0] = (self.pos[0] + self.vel[0]) % self.canvas.CANVAS_WIDTH
    self.pos[1] = (self.pos[1] - self.vel[1]) % self.canvas.CANVAS_HEIGHT
    return False

class Bullet(Sprite):
  RADIUS = 3
  LIFE = 35
  IMG_CENTER = [5, 5]
  IMG_SIZE = [10, 10]

  def __init__(self, pos, vel, ang, ang_vel, canvas):
    Sprite.__init__(self, pos, vel, ang, ang_vel, Bullet.RADIUS, canvas)
    self.img = Image.open('./images/shot2.png')
    self.age = 0

  def draw(self):
    upleft_x = self.pos[0] - Bullet.IMG_CENTER[0]
    upleft_y = self.pos[1] - Bullet.IMG_CENTER[1]
    self.image = ImageTk.PhotoImage(self.img) # bullet do not need rotate
    self.canvas.create_image(upleft_x, upleft_y, anchor=Tkinter.NW, image=self.image)

  def update(self):
    # update position
    self.age += 1
    if self.age > Bullet.LIFE:
        return True

    self.pos[0] = (self.pos[0] + self.vel[0]) % self.canvas.CANVAS_WIDTH
    self.pos[1] = (self.pos[1] - self.vel[1]) % self.canvas.CANVAS_HEIGHT
    return False