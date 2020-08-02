import pygame
import random
import math
import time
from Robot import Robot
from Resources import InfoPacket, WheelInfo, Mode, State, Logger, Colors
from WallMap import WallMap
# from WallMapCython import WallMap
# from cythonized_files.WallMapCython import WallMap
# from WallMapCython import WallMap
# from WallMap import WallMap

#Window
screen_width = 1440
screen_height = 800
all_buttons = []

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("GroundStation")
clock = pygame.time.Clock()

ROBOT = pygame.image.load('./ground_station/assets/Robot.png')
COMPASS = pygame.image.load('./ground_station/assets/Compass.png')
mediumFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("./ground_station/assets/OpenSans-Regular.ttf", 40)

#information about the robot and location
mode = Mode.manual

#objects that we need
robot = Robot(image = ROBOT)
logger = Logger("BotDisplay")
wall_map = WallMap()

def main():
  global robot, mode, screen, screen_width, screen_height
  start_time = int(round(time.time() * 1000))
  previous_time = start_time
  while True:
    #Check for user input on the keyboard and OSX operations
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quitProgram()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            quitProgram()
        elif event.type == pygame.VIDEORESIZE:
          screen_width, screen_height = event.size
          screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    
    #Draw the buttons and header on the screen
    top_bar_y = 1/20
    screen.fill(Colors.BLACK)
    pygame.draw.rect(screen, Colors.DBLACK, (0, 0, screen_width, screen_height * top_bar_y * 2))#top black bar
    
    mode_button_height = .1
    mode_button_y_diff = mode_button_height+.01
    mode_button_x = .89
    create_button_from_text("Stop", mode_button_x, .1 + mode_button_y_diff * 0, .1, mode_button_height, mediumFont, text_color=Colors.BLACK, background_color=Colors.DBLUE)
    create_button_from_text("Explore", mode_button_x, .1 + mode_button_y_diff * 1, .1, mode_button_height, mediumFont, text_color=Colors.BLACK, background_color=Colors.DBLUE)
    create_button_from_text("Sweep", mode_button_x, .1 + mode_button_y_diff * 2, .1, mode_button_height, mediumFont, text_color=Colors.BLACK, background_color=Colors.DBLUE)
    create_button_from_text("Manual", mode_button_x, .1 + mode_button_y_diff * 3, .1, mode_button_height, mediumFont, text_color=Colors.BLACK, background_color=Colors.DBLUE)
    
    mode_label = draw_text("Mode: " + Mode.all_modes_english[mode], .91, top_bar_y, text_color=Colors.PINK)
    draw_text("State: " + State.all_states_english[robot.state], .75, top_bar_y, text_color=Colors.PINK)
    draw_text(str(robot.dataPackets[-1].right_encoder_counts), .5, top_bar_y, text_color=Colors.PINK)
    draw_text(str(robot.dataPackets[-1].left_encoder_counts), .3, top_bar_y, text_color=Colors.PINK)
    # draw_text(current_action, .01, top_bar_y, basis_point='midleft', text_color=Colors.PINK)
    
    #Draw interactive elements
    #x_max is .85, y_min is .1
    change_mode_from_button()

    if mode == Mode.manual:
      robot.change_state(state_from_key_press())
      pass
    elif mode == Mode.explore:
      pass
    elif mode == Mode.sweep:
      pass
    elif mode == Mode.stop:
      robot.change_state(State.stop)
    
    new_points = robot.add_data()
    if new_points is not None:
      for point in new_points:
        wall_map.add_obstacle_point(point[0], point[1])

    angle = random.uniform(0, 2 * math.pi)
    x = 5 * math.cos(angle)
    y = 5 * math.sin(angle)
    wall_map.add_obstacle_point(x, y)
    # wall_map.add_obstacle_point(0, 0)
    # wall_map.add_obstacle_point(10, 10)
    # wall_map.add_obstacle_point(-10, -10)
    # wall_map.add_obstacle_point(0, 10)
    # wall_map.add_obstacle_point(0, -10)
    # wall_map.add_obstacle_point(0, 10)
    # wall_map.add_obstacle_point(10, 10)
    # wall_map.add_obstacle_point(50, 0)
    # if int(round(time.time() * 1000)) - previous_time >= 0:
    #   previous_time = int(round(time.time() * 1000))
    #   wall_map.add_obstacle_point(random.randint(-50, 50), random.randint(-50, 50))
      
    
    wall_map.draw_map(screen=screen, x_min=0 * screen_width, x_max=1 * screen_width, y_min=0 * screen_height, y_max=1 * screen_height)
    robot.draw_robot(screen=screen, x_min=0 * screen_width, x_max=1 * screen_width, y_min=0 * screen_height, y_max=1 * screen_height)
    # wall_map.draw_map(screen=screen, x_min=0 * screen_width, x_max=(mode_button_x - .01) * screen_width, y_min=(top_bar_y * 2 + .01) * screen_height, y_max=1 * screen_height)
    # robot.draw_robot(screen=screen, x_min=0 * screen_width, x_max=(mode_button_x - .01) * screen_width, y_min=(top_bar_y * 2 + .01) * screen_height, y_max=1 * screen_height)
    draw_compass(screen_width-175, screen_height-175, robot.angle)
    pygame.display.flip()
  print("Total time taken:", int(round(time.time() * 1000)) - start_time)
  quitProgram()
  
def create_button_from_text(text, x, y, width, height, font_object, text_color=Colors.WHITE, background_color=Colors.BLACK):
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
      
def draw_text(text, x, y, font_object=mediumFont, text_color=Colors.WHITE, basis_point='center', background_color=Colors.BLACK):
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
  half_image = COMPASS.get_size()[0] / 2
  screen.blit(COMPASS, (x, y)) #Draws the compass image
  #logger.log("x, y, angle:", x, y, angle)
  pygame.draw.line(screen, Colors.GREEN, (x+half_image, y+half_image), (x+half_image + (65*math.cos(math.radians(-(angle+90)))), y+half_image + (65*math.sin(math.radians(-(angle+90))))), width=2)

def quitProgram(): #Quits Pygame and Python
  global robot
  # Logger.log("Stopping all tasks and quitting program")
  logger.log("Stopping all tasks and quitting program")
  robot.quitProgram()
  pygame.quit()
  quit()

def change_mode_from_button():
  global all_buttons, mode
  temp = get_button_pressed()
  if temp is not None: #if a button was pressed, continue with this section
    pressed_button = temp[0]
    button_text = temp[1]
    mode = Mode.all_modes.index(button_text)
    logger.log("Mode changed to: " + Mode.all_modes[mode])
    
main()