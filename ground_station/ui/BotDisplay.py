import pygame as pg 
import random 
import numpy as np
import math as m

#Colors
BLACK = (30, 30, 30)
WHITE = (167, 167, 167)
GREEN = (75, 192, 168)
DBLUE = (0, 116, 194)
TAN = (184, 130, 109)
BLUE = (85, 154, 212)
PINK = (197, 134, 192)

#Main Settings
SCREEN_WIDTH = 1440 #Must be divisible by SQUARE_SIZE
SCREEN_HEIGHT = 800 #Must be divisible by SQUARE_SIZE
FPS = 60 #Standard Smooth FPS
running = True

def quitProgram(): #Quits Pygame and Python
  pg.quit()
  quit()

def backgroundInputCheck(eventList): #Constantly checks for quits and enters
  #For the buttons to close, minimize, and maximize the window
  for event in eventList:
          if event.type == pg.QUIT:
              quitProgram()
          elif event.type == pg.KEYDOWN:
              if event.key == pg.K_ESCAPE:
                  quitProgram()

def writeText(screen, font, size, text, x, y, color):
  smallText = pg.font.SysFont(font, size)
  textSurf = smallText.render(text, True, color)
  textRect = textSurf.get_rect()
  textRect.center = (x, y)
  screen.blit(textSurf, textRect)

def button_press(msg, x, y, w, h, ic, ac): #Button that loops through options, like in settings
  """
  msg is the text on the buttons
  x is the x position on the screen of the center of the button
  y is the y position on the screen of the center of the button
  w is width
  h is heigt
  ic is the initial color
  ac is the hover color
  """
  font = 'hermann'
  writeText(screen, font, 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
  
  mouse = pg.mouse.get_pos()
  click = pg.mouse.get_pressed()
  
  if x+w > mouse[0] > x and y+h > mouse[1] > y:
      pg.draw.rect(screen, ac,(x,y,w,h))
      if click[0] == 1:
          return True
  else:
      pg.draw.rect(screen, ic,(x,y,w,h))
  writeText(screen, font, 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
  return False
  
def createButton(text, x, y, w, h, ic, ac, action = None): #Normal button that preforms an action
  global PLAYER, PLAYER_CONTROLLED
  mouse = pg.mouse.get_pos()
  click = pg.mouse.get_pressed()
  if x+w > mouse[0] > x and y+h > mouse[1] > y:
      pg.draw.rect(screen, ac,(x,y,w,h))
      if click[0] == 1 and action != None:
          action()
  else:
      pg.draw.rect(screen, ic,(x,y,w,h))
  writeText(screen, "arial", 50, text, (x+(w/2)), (y+(h/2)), WHITE)
  
def mainScreen():
  while running:
      RUNNING = backgroundInputCheck(pg.event.get())
      
      screen.fill(BLACK) #Paint the whole screen black

      clock.tick(60)
      pg.display.flip()

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("GroundStation")
clock = pg.time.Clock()
mainScreen()