import pygame as pygame
import random 
import numpy as np
import math
from GroundStation import Mode, State
from Communicator import Communicator

#Colors
BLACK = (30, 30, 30)
DBLACK = (10, 10, 10)
WHITE = (167, 167, 167)
GREEN = (75, 192, 168)
DBLUE = (0, 116, 194)
TAN = (184, 130, 109)
BLUE = (85, 154, 212)
PINK = (197, 134, 192)

#Window
SCREEN_WIDTH = 1440 
SCREEN_HEIGHT = 800 
FPS = 60 #Standard Smooth FPS


# pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GroundStation")

clock = pygame.time.Clock()
COMPASS = pygame.image.load('./ground_station/assets/Compass.png')
mediumFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 40)

#information about the robot
running = True
mode = Mode.manual
state = State.stop


#objects that we need
communicator = Communicator()

def main():
  while running:
    #check to see if the user wants to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quitProgram()
        elif event.type == pg.KEYDOWN:
          if event.key == pg.K_ESCAPE:
            quitProgram()
    
    screen.fill(BLACK)
    pg.draw.rect(screen, DBLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT/11))
    draw_compass(SCREEN_WIDTH-175, SCREEN_HEIGHT-175)

    if mode == Mode.manual:
      state = state_from_key_press()
      print(State.all_states[state])

    communicator.transmit_info()
    pygame.display.flip()
      
  
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

def state_from_key_press():
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    return State.turn_left
  elif keys[pygame.K_RIGHT]:
    return State.turn_right
  elif keys[pygame.K_UP]:
    return State.forward
  elif keys[pygame.K_DOWN]:
    return State.reverse
  else:
    return State.stop
def draw_compass(x, y, angle = 90.0):
  screen.blit(COMPASS, (x, y))
  pygame.draw.line(screen, PINK, (x+72, y+72), (x+72 + (65*math.cos(math.radians(angle-90))), y+72 + (65*math.sin(math.radians(angle-90)))), 8)

def quitProgram(): #Quits Pygame and Python
  pygame.quit()
  quit()
  communicator.deactivate_bluetooth()
  #todo: quit bluetooth comms


main()

# def createButton(text, x, y, w, h, ic, ac, action = None): #Normal button that preforms an action
#   mouse = pg.mouse.get_pos()
#   click = pg.mouse.get_pressed()
#   if x+w > mouse[0] > x and y+h > mouse[1] > y:
#       pg.draw.rect(screen, ac,(x,y,w,h))
#       if click[0] == 1 and action != None:
#           action()
#   else:
#       pg.draw.rect(screen, ic,(x,y,w,h))
#   writeText(screen, "arial", 50, text, (x+(w/2)), (y+(h/2)), WHITE)



#   def button_press(msg, x, y, w, h, ic, ac): #Button that loops through options, like in settings
#   """
#   msg is the text on the buttons
#   x is the x position on the screen of the center of the button
#   y is the y position on the screen of the center of the button
#   w is width
#   h is heigt
#   ic is the initial color
#   ac is the hover color
#   """
#   font = 'hermann'
#   writeText(screen, font, 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
  
#   mouse = pg.mouse.get_pos()
#   click = pg.mouse.get_pressed()
  
#   if x+w > mouse[0] > x and y+h > mouse[1] > y:
#       pg.draw.rect(screen, ac,(x,y,w,h))
#       if click[0] == 1:
#           return True
#   else:
#       pg.draw.rect(screen, ic,(x,y,w,h))
#   writeText(screen, font, 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
#   return False


# def mainScreen():
#   while running:
#     if(): #If state is manual
#       newState = manual_input_check(pg.event.get())
#       #change ground station state to newState
      
#     screen.fill(BLACK) #Paint the whole screen black
      
#     pg.draw.rect(screen, DBLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT/11))
#     draw_compass(SCREEN_WIDTH-175, SCREEN_HEIGHT-175)
#     #writeText(screen, 'hermann', 75, "CONNECTED", 150, 50, DBLUE)
      
#     clock.tick(60)
#     pg.display.flip()


# def writeText(screen, font, size, text, x, y, color):
#   smallText = pg.font.SysFont(font, size)
#   textSurf = smallText.render(text, True, color)
#   textRect = textSurf.get_rect()
#   textRect.center = (x, y)
#   screen.blit(textSurf, textRect)


# def manual_input_check(eventList): #Constantly checks for quits and enters
#   #For the buttons to close the window
#   for event in eventList:
#           if event.type == pg.QUIT:
#               quitProgram()
#               return 0
#           elif event.type == pg.KEYDOWN:
#               if event.key == pg.K_ESCAPE:
#                   quitProgram()
#                   return 0
#               elif event.key == pg.K_w:
#                   return 1
#               elif event.key == pg.K_a:
#                   return 3
#               elif event.key == pg.K_s:
#                   return 2
#               elif event.key == pg.K_d:
#                   return 4
#               else:
#                   return 0
                
# def background_input_check(eventList): #Constantly checks for quits and enters
#   #For the buttons to close the window
#   for event in eventList:
#           if event.type == pg.QUIT:
#               quitProgram()
#           elif event.type == pg.KEYDOWN:
#               if event.key == pg.K_ESCAPE:
#                   quitProgram()