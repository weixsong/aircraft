import Tkinter

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
    self.centerWindow()

    self.parent.bind('<Key>', self.key)
    self.parent.bind('<Motion>', self.motion)

    self.canvas = MyCanvas(self, width=MyCanvas.CANVAS_WIDTH, height=MyCanvas.CANVAS_HEIGHT, 
      background='black')
    self.canvas.pack(side=Tkinter.TOP)
    self.canvas.draw()

    self.label_mouse = Tkinter.Label(self, text="mouse", background='white')
    self.label_mouse.pack(side=Tkinter.RIGHT, expand=1)

    self.label_key = Tkinter.Label(self, text="key", background='white')
    self.label_key.pack(side=Tkinter.RIGHT, expand=1)

    self.label_info = Tkinter.Label(self, text="info", background='white')
    self.label_info.pack(side=Tkinter.RIGHT, expand=1)

  def centerWindow(self):
    sw = self.parent.winfo_screenwidth()
    sh = self.parent.winfo_screenheight()
        
    x = (sw - Window.WINDOW_WIDTH) / 2
    y = (sh - Window.WINDOW_HEIGHT) / 2
    geo = '{0}x{1}+{2}+{3}'.format(str(Window.WINDOW_WIDTH), str(Window.WINDOW_HEIGHT), str(x), str(y))
    self.parent.geometry(geo)

  def key(self, event):
    self.parent.event_generate('<Motion>', warp=True, x=50, y=50)

  def motion(self, event):
    self.label_mouse.config(text='mouse x:{}, y:{}'.format(event.x, event.y))

class MyCanvas(Tkinter.Canvas):
  CANVAS_WIDTH = 800
  CANVAS_HEIGHT = 600

  def __init__(self, root,  cnf={}, **args):
    Tkinter.Canvas.__init__(self, root, cnf={}, **args)

  def draw(self):
    # below code is a test of canvas
    self.create_rectangle(0, 10, 120, 80, outline="#fb0", fill="#fb0")
    self.create_rectangle(150, 0, 240, 80, outline="#f50", fill="#f50")
    self.create_rectangle(270, 10, 370, 80, outline="#05f", fill="#05f")

if __name__ == '__main__':
  root = Tkinter.Tk()
  window = Window(root)
  root.mainloop()