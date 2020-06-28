import pygame as pygame
import random 
import numpy as np
import math
import time
#from Communicator import Communicator
from Robot import Robot, Mode, State
    
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
screen_width = 1440 
screen_height = 800 
FPS = 60 #Standard Smooth FPS


# pygame initialization
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("GroundStation")

clock = pygame.time.Clock()
COMPASS = pygame.image.load('./ground_station/assets/Compass.png')
ROBOT = pygame.image.load('./ground_station/assets/Robot.png')
mediumFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 40)

#information about the robot
running = True
mode = Mode.manual
current_action = 'Initializing Ground Station'

#time information for communications
start_time = int(round(time.time() * 1000))
last_communication_time = 0
last_button_press_time = 0
#print("Start Time" + str(start_time))

#objects that we need
robot = Robot()

#dictionary won't work because pygame.Rect is unhashable
all_buttons = []

def main():
  # raise Exception("Into the unknowwowowowowoowowwwon")
  global last_communication_time, running, robot, last_button_press_time, mode, current_action, screen, screen_width, screen_height
  while running:
    #check to see if the user wants to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quitProgram()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            quitProgram()
        elif event.type == pygame.VIDEORESIZE:
          screen_width, screen_height = event.size
          screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    
    
    top_row_y = 1/20
    #painting screen components
    screen.fill(BLACK)
    pygame.draw.rect(screen, DBLACK, (0, 0, screen_width, screen_height / 10))#top black bar
    mode_button_height = .1
    mode_button_y_diff = mode_button_height+.01
    create_button_from_text("Stop", .89, .1 + mode_button_y_diff * 0, .1, mode_button_height, mediumFont, text_color=BLACK, background_color=DBLUE)
    create_button_from_text("Explore", .89, .1 + mode_button_y_diff * 1, .1, mode_button_height, mediumFont, text_color=BLACK, background_color=DBLUE)
    create_button_from_text("Sweep", .89, .1 + mode_button_y_diff * 2, .1, mode_button_height, mediumFont, text_color=BLACK, background_color=DBLUE)
    create_button_from_text("Manual", .89, .1 + mode_button_y_diff * 3, .1, mode_button_height, mediumFont, text_color=BLACK, background_color=DBLUE)
    
    mode_label = draw_text("Mode: " + Mode.all_modes[mode], .91, top_row_y, text_color=PINK)
    draw_text("State: " + State.all_states[robot.state], .75, top_row_y, text_color=PINK)
    draw_text(current_action, .01, top_row_y, basis_point='midleft', text_color=PINK)
    draw_compass(screen_width-175, screen_height-175)


    draw_robot(0, .89, 1/10, 1)
    #user interaction

    #button presses
    current_time = get_time()
    #one sec I have to glue and drill the last thing into my boat bc my dad goes to sleep early and we are going on the boat tomorrow so like 15 min 
    temp = get_button_pressed()
    if temp is not None: #if a button was pressed, continue with this section
      pressed_button = temp[0]
      button_text = temp[1]
      if current_time - last_button_press_time > 250:
        last_button_press_time = current_time
        mode = Mode.all_modes.index(button_text)
        log_action("Mode changed to: " + Mode.all_modes[mode])
      
    #change state depending on the mode
    if mode == Mode.manual:
      if(get_time() - last_communication_time > 100): #What is this increment for?
        if(robot.change_state(state_from_key_press())): #returns true if necessary
          log_action("State changed to: " + State.all_states[robot.state] + ", transmission at: " + str(current_time))
          last_communication_time = get_time()
    
    pygame.display.flip()
  quitProgram()
  
def create_button_from_text(text, x, y, width, height, font_object, text_color=WHITE, background_color=BLACK):
  """
  x and y refer to the coordinate point of the top left of the button, where (0,0) is the top-left
  corner and (1,1) is the bottom right corner
  width and height refer to the width and height of the button, where 0 represents no width or height,
  and 1 represent a button that will fill up the screen (same width and height as the screen)
  """
  new_button = pygame.Rect((screen_width * x), (screen_height * y), screen_width * width, screen_height * height)
  playX = mediumFont.render(text, True, text_color, background_color)
  playXRect = playX.get_rect()
  playXRect.center = new_button.center
  pygame.draw.rect(screen, background_color, new_button)
  screen.blit(playX, playXRect)
  all_buttons.append((new_button, text))
  return new_button

def get_button_pressed():
  """
  Returns the button pressed. If no button is pressed, it will return None
  If multiple buttons are pressed, it will return a list of all pressed buttons.
  The only way that I can think of where this would happen is if buttons overlapped.
  """
  click, _, _ = pygame.mouse.get_pressed()
  if click == 1:
    mouse = pygame.mouse.get_pos()
    for button, text in all_buttons:
      if button.collidepoint(mouse):
        return button, text
      
def draw_text(text, x, y, font_object=mediumFont, text_color=WHITE, basis_point = 'center'):
  title = font_object.render(text, True, text_color)
  titleRect = title.get_rect()
  if basis_point == 'center':
    titleRect.center = (screen_width * x, screen_height * y)
  elif basis_point == 'topleft':
    titleRect.topleft = (screen_width * x, screen_height * y)
  elif basis_point == 'topright':
    titleRect.topright = (screen_width * x, screen_height * y)
  elif basis_point == 'bottomleft':
    titleRect.bottomleft = (screen_width * x, screen_height * y)
  elif basis_point == 'bottomright':
    titleRect.bottomright = (screen_width * x, screen_height * y)
  elif basis_point == 'midleft':
    titleRect.midleft = (screen_width * x, screen_height * y)
  elif basis_point == 'midright':
    titleRect.midright = (screen_width * x, screen_height * y)
  elif basis_point == 'midtop':
    titleRect.midtop = (screen_width * x, screen_height * y)
  elif basis_point == 'midbottom':
    titleRect.midbottom = (screen_width * x, screen_height * y)
  screen.blit(title, titleRect)
  return titleRect

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
  pygame.draw.line(screen, GREEN, (x+72, y+72), (x+72 + (65*math.cos(math.radians(angle-90))), y+72 + (65*math.sin(math.radians(angle-90)))), 8)

def get_time():
  return int(round(time.time() * 1000)) - start_time

def quitProgram(): #Quits Pygame and Python
  print("Stopping all tasks and quitting program")
  robot.communicator.transmit_info(State.stop)
  pygame.quit()
  robot.communicator.deactivate_bluetooth()
  quit()

def log_action(action):
  global current_action
  print(action)
  current_action = action

def draw_robot(x_min, x_max, y_min, y_max):
  x_min = screen_width * x_min
  x_max = screen_width * x_max
  y_min = screen_height * y_min
  y_max = screen_height * y_max
  screen.blit(ROBOT, (robot.xcoord, robot.ycoord))

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