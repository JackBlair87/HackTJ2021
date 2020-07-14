from Resources import Logger, Colors
import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
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

  def draw_wall(self, screen, y_max, x_add_num, x_scale, x_screen_adjustment, y_add_num, y_scale, y_screen_adjustment):
    screen_points = []
    for point in self.points:
      x = point[0]
      y = point[1]

      x += x_add_num
      x *= x_scale
      x += x_screen_adjustment

      y += y_add_num
      y *= y_scale
      y += y_screen_adjustment

      # self.logger.log("adding point", point[0], point[1], "on r,c  at", x, y)
      screen_points.append( (x, y_max - y) ) #correct the order (x, y) to (r, c)
    self.logger.log("going to draw wall now, len(self.points) - 1 is ", len(self.points) - 1)
    if len(self.points) > 2:
      self.logger.log("Adding wall at ", screen_points)
      pygame.draw.polygon(surface=screen, color=Colors.RED, points=screen_points, width=10)
    # pygame.draw.line(surface=screen, color=Colors.BLUE, start_pos=(x_start, y_start), end_pos=(x_stop, y_stop), width=8)

class WallMap:
  """
  todo: Think about using an auxilary set to hold raw data points. Whenever possible,
  calculate a regression and the regression lines to another set with regressions. This would mean more processing
  upfront, but it would save a lot of memory.
  The line regression would have the regression, as well as the start and and and coordinates.
  """
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
    # self.logger.log("adding point (" + str(x) + ', ' + str(y))
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

      min_distance = float('inf')
      wall_to_add = None
      for wall in self.walls:
        distance = wall.calculate_distance(point)
        if distance < min_distance:
          min_distance = distance
          wall_to_add = wall
      if min_distance < 5: #if it is close enough to another wall, add it to that wall
        wall_to_add.add_point(point)
      else: #otherwise make a new wall with this point
        self.walls.add(Wall(point))

    # self.walls.add(Wall(self.obstacle_points))

  def print_map(self):
    for row in self.map:
      self.logger.log(row)
  
  def draw_map_stable(self, screen, x_min, x_max, y_min, y_max):
    #parameters are given as actual dimensions, not from 0 to 1
    print("draw_map_stable called with", x_min, x_max, y_min, y_max)
    screen_width = x_max - x_min
    screen_height = y_max - y_min
    # screen_ratio = screen_width / screen_height

    map_width = self.x_max - self.x_min
    map_height = self.y_max - self.y_min
    # map_ratio = map_width / map_height

    x_add_num = -1 * self.x_min
    x_scale = screen_width / map_width

    y_add_num = -1 * self.y_min
    y_scale = screen_height / map_height

    x_screen_adjustment = 0
    y_screen_adjustment = 0

    if y_scale > x_scale:
      self.logger.log("adjusting y_scale")
      y_screen_adjustment = (screen_height - screen_width) / 2
      y_scale = x_scale
    else:
      self.logger.log("adjusting x_scale")
      #scale_ratio = (x_scale - y_scale) / 2
      x_screen_adjustment = (screen_width - screen_height) / 2
      x_scale = y_scale
    
    #self.logger.log("x bounds:", x_min, x_max)
    #self.logger.log("y bounds:", y_min, y_max)
    #self.logger.log("self.x bounds", self.x_min, self.x_max)
    #self.logger.log("self.y bounds", self.y_min, self.y_max)
    for point in self.obstacle_points:
      x = point[0]
      y = point[1]

      x += x_add_num
      x *= x_scale
      x += x_screen_adjustment

      y += y_add_num
      y *= y_scale
      y += y_screen_adjustment

      # self.logger.log("adding point", point[0], point[1], "on r,c  at", x, y)
      center = (x, y_max - y) #correct the order (x, y) to (r, c)
      # self.logger.log("adding point", point[0], point[1], "on x, y  at", x, y)
      pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=10)
    for wall in self.walls:
      # self.logger.log("start, stop of wall", wall.start, wall.stop)
      # wall.draw_wall(screen=screen, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, x_add_num=x_add_num, x_scale=x_scale, x_screen_adjustment=x_screen_adjustment, y_add_num=y_add_num, y_scale=y_scale, y_screen_adjustment=y_screen_adjustment)
      wall.draw_wall(screen=screen, y_max=y_max, x_add_num=x_add_num, x_scale=x_scale, x_screen_adjustment=x_screen_adjustment, y_add_num=y_add_num, y_scale=y_scale, y_screen_adjustment=y_screen_adjustment)


  def draw_map(self, screen, x_min, x_max, y_min, y_max):
    #parameters are given as actual dimensions, not from 0 to 1
    print("draw_map called with", x_min, x_max, y_min, y_max)
    screen_width = x_max - x_min
    screen_height = y_max - y_min

    map_width = self.x_max - self.x_min
    map_height = self.y_max - self.y_min

    x_add_num = -1 * self.x_min
    x_scale = screen_width / map_width

    y_add_num = -1 * self.y_min
    y_scale = screen_height / map_height

    x_screen_adjustment = 0
    y_screen_adjustment = 0

    map_ratio = map_height / map_width
    screen_ratio = screen_height / screen_width

    if map_ratio > screen_ratio:
      self.logger.log("map_ratio > screen_ratio")
      ratio_difference = map_ratio - screen_ratio
      ratio_difference /= 2
      y_screen_adjustment += ratio_difference * y_scale
    elif map_ratio > screen_ratio:
      self.logger.log("screen_ratio > map_ratio")
      ratio_difference = screen_ratio - map_ratio
      ratio_difference /= 2
      x_screen_adjustment += ratio_difference * x_scale

    for point in self.obstacle_points:
      x = point[0]
      y = point[1]

      x += x_add_num
      x *= x_scale
      x += x_screen_adjustment

      y += y_add_num
      y *= y_scale
      y += y_screen_adjustment

      center = (x, y_max - y) #correct the order (x, y) to (r, c)
      pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=10)
    for wall in self.walls:
      wall.draw_wall(screen=screen, y_max=y_max, x_add_num=x_add_num, x_scale=x_scale, x_screen_adjustment=x_screen_adjustment, y_add_num=y_add_num, y_scale=y_scale, y_screen_adjustment=y_screen_adjustment)