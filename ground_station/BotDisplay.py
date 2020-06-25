import pygame as pg 
import random 
import numpy as np
import math as m

#Colors and fonts
BLACK = (30, 30, 30)
DBLACK = (10, 10, 10)
WHITE = (167, 167, 167)
GREEN = (75, 192, 168)
DBLUE = (0, 116, 194)
TAN = (184, 130, 109)
BLUE = (85, 154, 212)
PINK = (197, 134, 192)

mediumFont = pg.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pg.font.Font("OpenSans-Regular.ttf", 40)

#Main Settings
SCREEN_WIDTH = 1440 
SCREEN_HEIGHT = 800 
FPS = 60 #Standard Smooth FPS
running = True
COMPASS = pg.image.load('./ground_station/ui/Compass.png')

def quitProgram(): #Quits Pygame and Python
  pg.quit()
  quit()

def backgroundInputCheck(eventList): #Constantly checks for quits and enters
  #For the buttons to close the window
  
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
  mouse = pg.mouse.get_pos()
  click = pg.mouse.get_pressed()
  if x+w > mouse[0] > x and y+h > mouse[1] > y:
      pg.draw.rect(screen, ac,(x,y,w,h))
      if click[0] == 1 and action != None:
          action()
  else:
      pg.draw.rect(screen, ic,(x,y,w,h))
  writeText(screen, "arial", 50, text, (x+(w/2)), (y+(h/2)), WHITE)

def create_button_from_text(text, x, y, width, height):
  """
  x and y refer to the coordinate point of the top left of the button, where (0,0) is the top-left
  corner and (1,1) is the bottom right corner
  width and height refer to the width and height of the button, where 0 represents no width or height,
  and 1 represent a button that will fill up the screen (same width and height as the screen)
  """
  new_button = pg.Rect((SCREEN_WIDTH * x), (SCREEN_HEIGHT * x), SCREEN_WIDTH * width, SCREEN_HEIGHT * height)
  playX = mediumFont.render(text, True, DBLUE)
  playXRect = playX.get_rect()
  playXRect.center = new_button.center
  pg.draw.rect(screen, white, new_button)
  screen.blit(playX, playXRect)
  return new_button

  
def draw_compass(x, y, angle = 90.0):
  screen.blit(COMPASS, (x, y))
  pg.draw.line(screen, PINK, (x+72, y+72), (x+72 + (65*m.cos(-m.radians(angle))), y+72 + (65*m.sin(-m.radians(angle)))), 8)
      
  
def mainScreen():
  while running:
      RUNNING = backgroundInputCheck(pg.event.get())
      
      screen.fill(BLACK) #Paint the whole screen black
      
      pg.draw.rect(screen, DBLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT/11))
      draw_compass(SCREEN_WIDTH-175, SCREEN_HEIGHT-175)
      #writeText(screen, 'hermann', 75, "CONNECTED", 150, 50, DBLUE)
      
      clock.tick(60)
      pg.display.flip()

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("GroundStation")
clock = pg.time.Clock()
mainScreen()