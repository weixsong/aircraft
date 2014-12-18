import Tkinter

class Window(Tkinter.Frame):

  WINDOW_WIDTH = 800
  WINDOW_HEIGHT = 600 + 20

  WINDOW_X = 400
  WINDOW_Y = 400

  BACKGROUND = 'white'
  TITLE = 'AirCraft watkinsong@163.com'

  WINDOW = str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT) + '+' + str(WINDOW_X) + '+' + str(WINDOW_Y)

  def __init__(self, parent):
    Tkinter.Frame.__init__(self, parent, background=Window.BACKGROUND)
    self.parent = parent
    self.parent.title(Window.TITLE)
    self.pack(fill=Tkinter.BOTH, expand=1)
    self.parent.resizable(width=False, height=False)
    self.centerWindow()

  def centerWindow(self):
    sw = self.parent.winfo_screenwidth()
    sh = self.parent.winfo_screenheight()
        
    x = (sw - Window.WINDOW_WIDTH) / 2
    y = (sh - Window.WINDOW_HEIGHT) / 2
    geo = '{0}x{1}+{2}+{3}'.format(str(Window.WINDOW_WIDTH), str(Window.WINDOW_HEIGHT), str(x), str(y))
    self.parent.geometry(geo)

class Canvas(Tkinter.Frame):
  CANVAS_WIDTH = 800
  CANVAS_HEIGHT = 600
  pass


root = Tkinter.Tk()
window = Window(root)
#w = Tkinter.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background='white')
#w.pack()

#y = int(CANVAS_HEIGHT / 2)
#w.create_line(0, y, CANVAS_WIDTH, y, fill="#476042")

root.mainloop()
