import os, sys
import pygame
from ship import Ship
from utils import Util
from pygame.locals import *
from threading import Timer
import threading
from sprite import Rock
import random

class RockSpanTimer(threading.Thread):
  def __init__(self, controller, interval):
    threading.Thread.__init__(self)
    self.event = threading.Event()
    self.controller = controller
    self.interval = interval

  def run(self):
    while not self.event.is_set():
      """ The things I want to do go here. """
      self.controller.rock_spawner()
      self.event.wait(self.interval)

  def stop(self):
    self.event.set()

class Controller:
  WIDTH = 800
  HEIGHT = 600

  def __init__(self):
    self.screen = pygame.display.get_surface()
    self.area = self.screen.get_rect()
    self.lives = 3
    self.score = 0
    self.started = False

    self.splash, tmp = Util.load_image('splash.png')
    self.splash_pos = [self.screen.get_rect().width / 2 - tmp.width / 2, \
      self.screen.get_rect().height / 2 - tmp.height / 2]

    self.ship = Ship([400, 300], [0, 0], 0)
    self.allships = pygame.sprite.RenderPlain((self.ship,))

    self.rock_group = pygame.sprite.Group()
    self.missile_group = pygame.sprite.Group()
    self.explosion_group = pygame.sprite.Group()

  def new_game(self):
    self.lives = 3
    self.score = 0
    self.started = True
    self.ship = Ship([400, 300], [0, 0], 0)
    self.ship.set_game_status(True)
    self.allships = pygame.sprite.RenderPlain((self.ship,))

    self.rock_group = pygame.sprite.Group()
    self.missile_group = pygame.sprite.Group()
    self.explosion_group = pygame.sprite.Group()
    self.timer = RockSpanTimer(self, 1.5)
    self.timer.start()

  def game_over(self):
    self.timer.stop()
    self.ship.set_game_status(False)
    self.ship.set_thrust(False)
    self.is_started = False
    self.rock_group.empty()
    self.missile_group.empty()
    self.explosion_group.empty()

  def event_handler(self, event):
    if self.started == False and event.type == MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      inwidth = (400 - 400 / 2) < pos[0] < (400 + 400 / 2)
      inheight = (300 - 300 / 2) < pos[1] < (300 + 300 / 2)
      if (not self.started) and inwidth and inheight:
        print 'new game started'
        self.new_game()

    if self.started != True:
      return

    if event.type == QUIT:
      self.timer.stop()
      sys.exit()
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
      self.timer.stop()
      sys.exit()
    elif event.type == KEYDOWN and event.key == K_UP:
      self.ship.set_thrust(True)
    elif event.type == KEYDOWN and event.key == K_LEFT:
      self.ship.increment_angle_vel()
    elif event.type == KEYDOWN and event.key == K_RIGHT:
      self.ship.decrement_angle_vel()
    elif event.type == KEYUP and event.key == K_UP:
      self.ship.set_thrust(False)
    elif event.type == KEYUP and event.key == K_LEFT:
      self.ship.decrement_angle_vel()
    elif event.type == KEYUP and event.key == K_RIGHT:
      self.ship.increment_angle_vel()
    elif event.type == KEYUP and event.key == K_SPACE:
      missile = self.ship.shoot()
      self.missile_group.add(missile)

  def rock_spawner(self):
    if not self.started:
      return
    if len(self.rock_group.sprites()) >= Rock.LIMIT:
        return

    rock_pos = [random.randrange(0, self.area.width), random.randrange(0, self.area.height)]
    rock_vel = [random.random() * 1.3 - .3, random.random() * 1.3 - .3]
    rock_angle_vel = random.random() * 1.0 - .1

    add_vel = self.score * 0.5 + 1
    rock_vel = [rock_vel[0] * add_vel, rock_vel[1] * add_vel]
    rock = Rock(rock_pos, rock_vel, rock_angle_vel)

    distance = Util.dist(rock.rect.center, self.ship.rect.center)
    if distance < 200:
      return
    self.rock_group.add(rock)

  def update(self):
    self.allships.update()
    for missile in self.missile_group.sprites():
      if missile.update() == True:
        missile.kill()

    self.rock_group.update()

  def draw(self):
    self.allships.draw(self.screen)
    self.missile_group.draw(self.screen)
    self.rock_group.draw(self.screen)

    if self.started == False:
      self.screen.blit(self.splash, self.splash_pos)

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

  dubris, dubris_rect = Util.load_image('debris2_blue.png')
  screen.blit(dubris, (0, 0))
  pygame.display.flip()

  #Prepare Game Objects
  clock = pygame.time.Clock()

  #Main Loop
  counter = 0
  while 1:
    counter += 1
    clock.tick(60)
    for event in pygame.event.get():
      controller.event_handler(event)

    screen.blit(bg, (0, 0))
    wtime = (counter / 4) % screen.get_rect().width
    screen.blit(dubris, (wtime, 0))
    controller.update()
    controller.draw()
    pygame.display.flip()

if __name__ == '__main__':
  main()