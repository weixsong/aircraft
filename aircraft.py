import os
import pygame
from ship import Ship
from utils import Util
from pygame.locals import *

class Controller:
  WIDTH = 800
  HEIGHT = 600

  def __init__(self):
    self.ship = Ship([400, 300], [12, 0], 0)
    self.allships = pygame.sprite.RenderPlain((self.ship,))
    self.screen = pygame.display.get_surface()

  def update(self):
    self.allships.update()

  def draw(self):
    self.allships.draw(self.screen)

def main():
  pygame.init()
  os.environ['SDL_VIDEO_CENTERED'] = '1' # center the window
  screen = pygame.display.set_mode((Controller.WIDTH, Controller.HEIGHT))
  pygame.display.set_caption('Aircraft       watkinsong@163.com')
  pygame.mouse.set_visible(1)
  controller = Controller()

  bg, bg_rect = Util.load_image('nebula_blue.f2014.png')
  bg = bg.convert()

  screen.blit(bg, (0, 0))
  pygame.display.flip()

  #Prepare Game Objects
  clock = pygame.time.Clock()
  ship = Ship([400, 400], [12, 0], 0)
  allsprites = pygame.sprite.RenderPlain((ship,))

  #Main Loop
  while 1:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == QUIT:
        return
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        return
      elif event.type == KEYDOWN and event.key != K_ESCAPE:
        pass
      elif event.type == KEYUP and event.key != K_ESCAPE:
        print event.key
      elif event.type == MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        print pos
      elif event.type is MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        #print pos
      elif event.type is MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        #print pos

    controller.update()
    #allsprites.update()
    #Draw Everything
    screen.blit(bg, (0, 0))
    controller.draw()
    #allsprites.draw(screen)
    pygame.display.flip()

if __name__ == '__main__':
  main()