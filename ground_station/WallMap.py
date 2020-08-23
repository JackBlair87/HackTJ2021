from Resources import Logger, Colors
import pygame
# import matplotlib.pyplot as plt
import os
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
import math
from shapely.geometry import Polygon, Point, LineString

class Wall:
  def __init__(self, points):
    if type(points) is list:
      self.points = points
    else:
      self.points = [points]
    
    self.logger = Logger("Wall")
    
  def add_point(self, point):
    self.points.append(point)

  def calculate_distance(self, point):
    if len(self.points) == 1:
      x = self.points[0][0]
      y = self.points[0][1]
      wall_point = Point(x, y)
      input_point = Point(point[0], point[1])
      return wall_point.distance(input_point)
    elif len(self.points) == 2:
      wall_line = LineString(self.points)
      input_point = Point(point[0], point[1])
      return wall_line.distance(input_point)
    else:
      x = point[0]
      y = point[1]
      polygon = Polygon(self.points)
      return polygon.distance(Point(x, y))

  def calculate_distance_prerelease(self, point):
    # same situation here, peep the comment on draw_wall
    if len(self.points) == 1:
      x = self.points[0][0]
      y = self.points[0][1]
      wall_point = Point(x, y)
      input_point = Point(point[0], point[1])
      return wall_point.distance(input_point)
    elif len(self.points) == 2:
      wall_line = LineString(self.points)
      input_point = Point(point[0], point[1])
      return wall_line.distance(input_point)
    else:
      x = point[0]
      y = point[1]
      min_distance = float('inf')
      input_point = Point(point[0], point[1])
      for point1 in self.points:
        for point2 in self.points:
          if point1 is point2:
            continue
          wall_line = LineString([point1, point2])
          distance = wall_line.distance(input_point)
          if distance < min_distance:
            min_distance = distance
      return min_distance

  def draw_wall(self, screen, y_max, x_add_num, x_scale, x_screen_adjustment, y_add_num, y_scale, y_screen_adjustment):
    screen_points = []
    for x, y in self.points:
      x += x_add_num
      x *= x_scale
      x += x_screen_adjustment

      y += y_add_num
      y *= y_scale
      y += y_screen_adjustment

      screen_points.append( (x, y_max - y) ) #correct the order (x, y) to (r, c)
    if len(self.points) > 2:
      # self.logger.log("Adding wall at ", screen_points)
      pygame.draw.polygon(surface=screen, color=Colors.RED, points=screen_points, width=3)

class WallMap:
  def __init__(self, obstacle_points=set(), clear_rectangles=set()):
    self.logger = Logger("WallMap")
    self.obstacle_points = obstacle_points
    self.clear_rectangles = clear_rectangles
    self.walls = set()
    self.x_min = -10
    self.x_max = 10
    self.y_min = -10
    self.y_max = 10
    self.count_since_last_refresh = 0
  
  def add_obstacle_point(self, x, y):
    self.obstacle_points.add((x, y))
    if x > self.x_max - 10:
      self.x_max = x + 10
    if x < self.x_min + 10:
      self.x_min = x - 10
    
    if y > self.y_max - 10:
      self.y_max = y + 10
    if y < self.y_min + 10:
      self.y_min = y - 10
    
    if self.count_since_last_refresh >= 1:
      self.refresh_walls()
      self.count_since_last_refresh = 0
    else:
      self.count_since_last_refresh += 1
      
  def refresh_walls(self):
    for point in self.obstacle_points:
      if len(self.walls) == 0:
        self.walls.add(Wall(point))
        continue

      walls_to_add = []
      for wall in self.walls:
        distance = wall.calculate_distance(point)
        if distance < 5:
          walls_to_add.append(wall)
      if len(walls_to_add) == 1: #if it is close enough to another wall, add it to that wall
        walls_to_add[0].add_point(point)
      else: #otherwise make a new wall with this point
        total_points = []
        for adding_wall in walls_to_add: #combine walls if necessary
          total_points.extend(adding_wall.points)
          self.walls.discard(adding_wall)
        self.walls.add(Wall(total_points))
    self.obstacle_points = set()

  def draw_map(self, screen, x_min, x_max, y_min, y_max, robot):
                            # 0,   0,   1560, 1123
    #parameters are given as actual pixel dimensions, not from 0 to 1

    print('x_max:', x_max)
    print('y_max:', y_max)
    screen_width = x_max - x_min
    screen_height = y_max - y_min

    map_width = self.x_max - self.x_min
    map_height = self.y_max - self.y_min

    x_add_num = -1 * self.x_min
    x_scale = screen_width / map_width

    y_add_num = -1 * self.y_min
    y_scale = screen_height / map_height

    map_ratio = map_height / map_width
    screen_ratio = screen_height / screen_width

    if map_ratio > screen_ratio: # the map is taller than the screen, relatively
      y_scale = x_scale
    else:
      x_scale = y_scale
    
    # map_mid_x = self.x_min + map_width / 2
    # map_mid_y = self.y_min + map_height / 2

    # map_mid_x += x_add_num
    # map_mid_x *= x_scale

    # map_mid_y += y_add_num
    # map_mid_y *= y_scale

    # screen_mid_x = x_min + screen_width / 2
    # screen_mid_y = y_min + screen_height / 2

    x_screen_adjustment = 0
    y_screen_adjustment = 0

    # x_screen_adjustment = screen_mid_x - map_mid_x
    # y_screen_adjustment = screen_mid_y - map_mid_y

    # robot_x = (robot.location[0] - robot.size[0]/2 + x_add_num) * x_scale + x_screen_adjustment
    # robot_y = (robot.location[1] - robot.size[1]/2 + y_add_num) * y_scale + y_screen_adjustment

    # if robot_x > self.x_max - 10:
    #   self.x_max = robot_x + 10
    # if robot_x < self.x_min + 10:
    #   self.x_min = robot_x - 10
    
    # if robot_y > self.y_max - 10:
    #   self.y_max = robot_y + 10
    # if robot_y < self.y_min + 10:
    #   self.y_min = robot_y - 10
      
    # screen.blit(pygame.transform.rotate(robot.image, robot.angle), (robot_x, robot_y))
    for wall in self.walls:
      wall.draw_wall(screen=screen, y_max=y_max, x_add_num=x_add_num, x_scale=x_scale, x_screen_adjustment=x_screen_adjustment, y_add_num=y_add_num, y_scale=y_scale, y_screen_adjustment=y_screen_adjustment)
      for x, y in wall.points:
        self.logger.log('x 0:', x)
        x += x_add_num
        self.logger.log('x 1:', x)
        x *= x_scale
        self.logger.log('x 2:', x)
        x += x_screen_adjustment
        self.logger.log('x 3:', x)

        self.logger.log('y 0:', y)
        y += y_add_num
        self.logger.log('y 1:', y)
        y *= y_scale
        self.logger.log('y 2:', y)
        y += y_screen_adjustment
        self.logger.log('y 3:', y)

        print('y_max', y_max)

        center = (x, y_max - y) #correct the order (x, y) to (r, c)
        pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=5)