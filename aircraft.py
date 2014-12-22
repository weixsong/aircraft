import Tkinter
import Image 
import ImageTk
import tkFont
import random
from ship import Ship

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

    self.parent.bind('<Key>', self.on_key_down)
    self.parent.bind("<KeyRelease>", self.on_key_release)
    self.parent.bind('<Motion>', self.mouse_move)

    self.canvas = MyCanvas(self, width=MyCanvas.CANVAS_WIDTH, height=MyCanvas.CANVAS_HEIGHT, 
      background='black')
    self.canvas.pack(side=Tkinter.TOP)

    self.label_mouse = Tkinter.Label(self, text="mouse", background='white')
    self.label_mouse.pack(side=Tkinter.RIGHT, expand=1)

    self.label_key = Tkinter.Label(self, text="key", background='white')
    self.label_key.pack(side=Tkinter.RIGHT, expand=1)

    self.label_info = Tkinter.Label(self, text="info", background='white')
    self.label_info.pack(side=Tkinter.RIGHT, expand=1)

  def center_window(self):
    sw = self.parent.winfo_screenwidth()
    sh = self.parent.winfo_screenheight()
        
    x = (sw - Window.WINDOW_WIDTH) / 2
    y = (sh - Window.WINDOW_HEIGHT) / 2
    geo = '{0}x{1}+{2}+{3}'.format(str(Window.WINDOW_WIDTH), str(Window.WINDOW_HEIGHT), str(x), str(y))
    self.parent.geometry(geo)

  def on_key_down(self, event):
    self.label_key.config(text='key down: ' + str(event.keysym))

  def on_key_release(self, event):
    self.label_key.config(text='key up: ' + str(event.keysym))

  def mouse_move(self, event):
    self.label_mouse.config(text='mouse x:{}, y:{}'.format(event.x, event.y))

class MyCanvas(Tkinter.Canvas):
  CANVAS_WIDTH = 800
  CANVAS_HEIGHT = 600

  def __init__(self, root,  cnf={}, **args):
    Tkinter.Canvas.__init__(self, root, cnf={}, **args)

    self.background_img = Image.open("./images/nebula_blue.f2014.png")
    self.tatras = ImageTk.PhotoImage(self.background_img)
    self.debris_img = Image.open('./images/debris2_blue.png')
    self.debris = ImageTk.PhotoImage(self.debris_img)

    self.create_image(0, 0, anchor=Tkinter.NW, image=self.tatras)
    self.create_image(0, 0, anchor=Tkinter.NW, image=self.debris)

    self.font_size = 20
    self.font = tkFont.Font(family='Times',size=self.font_size, name="font%s" % self.font_size)
    self.time = 0

    self.x = 0 # for test
    self.ship = Ship([400, 300], [5, 4], 90, self)
    self.update()

  def update(self):
    self.delete('all')

    # animate the debris
    self.time += 1
    wtime = (self.time) % MyCanvas.CANVAS_WIDTH
    self.create_image(0, 0, anchor=Tkinter.NW, image=self.tatras)
    self.create_image(wtime, 0, anchor=Tkinter.NW, image=self.debris)

    # draw UI
    self.create_text(50, 30, text='Lives', fill='White', font=self.font)
    self.create_text(750, 30, text='Score', fill='White', font=self.font)

    # draw ship
    self.ship.draw()

    # ship update
    self.ship.update()

    # test
    self.create_rectangle(self.x, 450, 0, 480, outline='#fb0', fill='#fb0')
    self.x += 3
    if self.x > MyCanvas.CANVAS_WIDTH:
      self.x = 0
    self.after(100, self.update)

class GameController:
  def __init__(self):
    self.is_started = False
    self.lives = 3
    self.score = 0

    self.rock_group = set([])
    self.missile_group = set([])
    self.explosion_group = set([])

  def minus_live(self):
    self.lives -= 1

  def add_score(self):
    self.score += 1

if __name__ == '__main__':
  root = Tkinter.Tk()
  window = Window(root)
  root.mainloop()