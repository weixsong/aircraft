import Tkinter
import Image 
import ImageTk

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

    self.time = 0

    self.x = 0 # for test
    self.update()

  def update(self):
    self.delete('all')
    self.time += 1
    wtime = (self.time / 4) % MyCanvas.CANVAS_WIDTH
    self.create_image(0, 0, anchor=Tkinter.NW, image=self.tatras)
    self.create_image(wtime, 0, anchor=Tkinter.NW, image=self.debris)

    # test
    self.create_rectangle(self.x, 10, 0, 80, outline='#fb0', fill='#fb0')
    self.x += 3
    self.after(100, self.update)

if __name__ == '__main__':
  root = Tkinter.Tk()
  window = Window(root)
  root.mainloop()