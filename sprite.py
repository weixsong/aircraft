import Image 
import ImageTk
import Tkinter
from utils import Util
import math
import sound

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
    self.pos[1] = (self.pos[1] + self.vel[1]) % self.canvas.CANVAS_HEIGHT
    return False

class Bullet(Sprite):
  RADIUS = 3
  LIFE = 25
  IMG_CENTER = [5, 5]
  IMG_SIZE = [10, 10]

  def __init__(self, pos, vel, ang, ang_vel, canvas):
    Sprite.__init__(self, pos, vel, ang, ang_vel, Bullet.RADIUS, canvas)
    sound.missile.play()
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
    self.pos[1] = (self.pos[1] + self.vel[1]) % self.canvas.CANVAS_HEIGHT
    return False

class Explosion(Sprite):
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
