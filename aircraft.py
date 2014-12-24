import Tkinter
import Image 
import ImageTk
import tkFont
import random
from ship import Ship
from sprite import Rock
from sprite import Explosion
from utils import Util
from threading import Timer
import threading
import sound
import os

# cancel auto-repeat
os.system('xset r off')

class Window(Tkinter.Frame):

  WINDOW_WIDTH = 800
  WINDOW_HEIGHT = 600 + 20

  CANVAS_WIDTH = 800
  CANVAS_HEIGHT = 600

  BACKGROUND = 'white'
  TITLE = 'AirCraft watkinsong@163.com'

  def __init__(self, parent):
    Tkinter.Frame.__init__(self, parent, background=Window.BACKGROUND)
    self.parent = parent
    self.parent.title(Window.TITLE)
    self.pack(fill=Tkinter.BOTH, expand=1)
    self.parent.resizable(width=False, height=False)
    self.initUI()

  def initUI(self):
    self.center_window()

    self.canvas = MyCanvas(self, width=MyCanvas.CANVAS_WIDTH, height=MyCanvas.CANVAS_HEIGHT, 
      background='black')
    self.canvas.pack(side=Tkinter.TOP)

    self.label_mouse = Tkinter.Label(self, text="mouse", background='white')
    self.label_mouse.pack(side=Tkinter.RIGHT, expand=1)

    self.label_key = Tkinter.Label(self, text="key", background='white')
    self.label_key.pack(side=Tkinter.RIGHT, expand=1)

    self.label_info = Tkinter.Label(self, text="info", background='white')
    self.label_info.pack(side=Tkinter.RIGHT, expand=1)

    self.controller = GameController(self, self.canvas)
    self.canvas.set_controller(self.controller)
    self.parent.bind('<KeyPress>', self.controller.on_key_down)
    self.parent.bind("<KeyRelease>", self.controller.on_key_release)
    self.parent.bind('<Motion>', self.controller.mouse_move)
    self.parent.bind('<Button-1>', self.controller.mouse_click)

    self.canvas.update()

  def center_window(self):
    sw = self.parent.winfo_screenwidth()
    sh = self.parent.winfo_screenheight()
        
    x = (sw - Window.WINDOW_WIDTH) / 2
    y = (sh - Window.WINDOW_HEIGHT) / 2
    geo = '{0}x{1}+{2}+{3}'.format(str(Window.WINDOW_WIDTH), str(Window.WINDOW_HEIGHT), str(x), str(y))
    self.parent.geometry(geo)

class MyCanvas(Tkinter.Canvas):
  CANVAS_WIDTH = 800
  CANVAS_HEIGHT = 600

  def __init__(self, root, cnf={}, **args):
    Tkinter.Canvas.__init__(self, root, cnf={}, **args)

    self.background_img = Image.open("./images/nebula_blue.f2014.png")
    self.tatras = ImageTk.PhotoImage(self.background_img)
    self.debris_img = Image.open('./images/debris2_blue.png')
    self.debris = ImageTk.PhotoImage(self.debris_img)
    self.splash_img = Image.open('./images/splash.png')
    self.splash = ImageTk.PhotoImage(self.splash_img)

    self.font_size = 20
    self.font = tkFont.Font(family='Times',size=self.font_size, name="font%s" % self.font_size)
    self.time = 0

  def set_controller(self, controller):
    self.controller = controller

  def update(self):
    self.delete('all')

    # animate the debris
    self.time += 1
    wtime = (self.time / 4) % MyCanvas.CANVAS_WIDTH
    self.create_image(0, 0, anchor=Tkinter.NW, image=self.tatras)
    self.create_image(wtime, 0, anchor=Tkinter.NW, image=self.debris)

    # draw UI
    self.create_text(50, 30, text='Lives', fill='White', font=self.font)
    self.create_text(750, 30, text='Score', fill='White', font=self.font)
    self.create_text(50, 60, text=str(self.controller.lives), fill='White', font=self.font)
    self.create_text(750, 60, text=str(self.controller.score), fill='White', font=self.font)

    # draw ship
    self.controller.ship.draw()

    # ship update
    self.controller.ship.update()

    # rock update
    self.controller.process_sprite_group(self.controller.rock_group)
    self.controller.process_sprite_group(self.controller.missile_group)

    # collide detection
    if self.controller.group_collide(self.controller.rock_group, self.controller.ship) == True:
      self.controller.lives -= 1
      if self.controller.lives == 0:
        self.controller.game_over()

    num = self.controller.group_group_collide(self.controller.rock_group, self.controller.missile_group)
    self.controller.score += num

    self.controller.process_sprite_group(self.controller.explosion_group)

    # draw splash
    if not self.controller.is_started:
      self.create_image(400 - 200, 300 - 150, anchor=Tkinter.NW, image=self.splash)

    # call update
    self.after(16, self.update)

class Timer(threading.Thread):
  def __init__(self, controller):
    threading.Thread.__init__(self)
    self.event = threading.Event()
    self.controller = controller

  def run(self):
    while not self.event.is_set():
      """ The things I want to do go here. """
      self.controller.rock_spawner()
      self.event.wait(2)

  def stop(self):
    self.event.set()

class GameController(Tkinter.Frame):
  def __init__(self, window, canvas):
    Tkinter.Frame.__init__(self, window)
    self.window = window
    self.canvas = canvas

    self.ship = Ship([400, 300], [0, 0], 0, self.canvas)
    self.is_started = False
    self.lives = 3
    self.score = 0

    self.rock_group = set([])
    self.missile_group = set([])
    self.explosion_group = set([])

  def new_game(self):
    sound.soundtrack.play()
    self.ship = Ship([400, 300], [0, 0], 0, self.canvas)
    self.is_started = True
    self.lives = 3
    self.score = 0

    self.rock_group = set([])
    self.missile_group = set([])
    self.explosion_group = set([])
    self.rock_spawner()

  def game_over(self):
    sound.soundtrack.stop()
    self.rock_group = set([])
    self.missile_group = set([])
    self.explosion_group = set([])
    self.ship.set_thrust(False)
    #self.ship.set_game_state(False)
    self.ship.reset_angle_vel()
    self.is_started = False

  def minus_live(self):
    self.lives -= 1

  def add_score(self):
    self.score += 1

  def on_key_down(self, event):
    self.window.label_key.config(text='key down: ' + str(event.keysym))
    if self.is_started == False:
      return

    if event.keysym == 'Up':
      self.ship.set_thrust(True)
    if event.keysym == 'Left':
      self.ship.decrement_angle_vel()
    if event.keysym == 'Right':
      self.ship.increment_angle_vel()
    if event.keysym == 'space':
      self.ship.shoot(self.missile_group)

  def on_key_release(self, event):
    self.window.label_key.config(text='key up: ' + str(event.keysym))
    if self.is_started == False:
      return

    if event.keysym == 'Up':
      self.ship.set_thrust(False)
    if event.keysym == 'Left':
      self.ship.increment_angle_vel()
    if event.keysym == 'Right':
      self.ship.decrement_angle_vel()
    if event.keysym == 'space':
      pass

  def mouse_move(self, event):
    self.window.label_mouse.config(text='mouse x:{}, y:{}'.format(event.x, event.y))

  def mouse_click(self, event):
    self.window.label_mouse.config(text='mouse click x:{}, y:{}'.format(event.x, event.y))
    inwidth = (400 - 400 / 2) < event.x < (400 + 400 / 2)
    inheight = (300 - 300 / 2) < event.y < (300 + 300 / 2)
    if (not self.is_started) and inwidth and inheight:
      self.new_game()

  def rock_spawner(self):
    if self.is_started:
      rock_pos = [random.randrange(0, self.canvas.CANVAS_WIDTH), random.randrange(0, self.canvas.CANVAS_HEIGHT)]
      rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
      rock_avel = random.random() * .2 - .1

      add_vel = self.score * 0.5 + 1
      rock_vel = [rock_vel[0] * add_vel, rock_vel[1] * add_vel]
      rock = Rock(rock_pos, rock_vel, 0, rock_avel, self.canvas)

      if len(self.rock_group) >= Rock.LIMIT:
        self.after(1500, self.rock_spawner)
        return
      distance = Util.dist(rock.get_position(), self.ship.get_position())
      if distance < 200:
        self.after(1500, self.rock_spawner)
        return
      self.rock_group.add(rock)
      self.after(1500, self.rock_spawner)

  def process_sprite_group(self, group):
    for drawable in list(group):
      if drawable.update() == True:
        group.remove(drawable)
        continue
      drawable.draw()

  def group_group_collide(self, group1, group2):
    num = 0
    for item in list(group1):
      res = self.group_collide(group2, item)
      if res == True:
        group1.discard(item)
        num += 1        
    return num

  def group_collide(self, group, other):
    collide = False
    for e in list(group):
      if e.collide(other) == True:
        collide = True
        group.remove(e)
        explosion = Explosion(e.get_position(), self.canvas)
        self.explosion_group.add(explosion)

    return collide

if __name__ == '__main__':
  root = Tkinter.Tk()
  window = Window(root)
  root.mainloop()
