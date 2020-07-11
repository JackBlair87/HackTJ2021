from Resources import Logger, Colors
import pygame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import math
  
class Wall:
  def __init__(self):
    self.regression = LinearRegression()
    self.slope = None #these 
    self.b = None
    self.x_points = []
    self.y_points = []
    self.min = (-float('inf'), -float('inf'))
    self.max = (float('inf'), float('inf'))
    self.logger = Logger("Wall")

    
  def add_point(self, x, y, update_regression=False):
    self.x_points.append([x])
    self.y_points.append([y])
    if update_regression:
      self.update_regression()
  
  def update_regression(self, x_train=[], y_train=[]):
    x_train = [[elem] for elem in x_train]
    y_train = [[elem] for elem in y_train]
    self.x_points.extend(x_train)
    self.y_points.extend(y_train)

    self.regression.fit(self.x_points, self.y_points)
    slope = round(self.regression.coef_[0][0], 4)

    if slope > 100:
      self.slope = float('inf')
      self.b = None

      average_x = sum(self.x_points) / len(self.x_points)
      self.min = (average_x, min(self.y_points))
      self.max = (average_x, max(self.y_points))
    else:
      self.slope = slope
      self.b = round(self.regression.intercept_[0], 4)
      min_x = min(self.x_points)
      max_x = max(self.x_points)
      self.start = (min_x[0], self.regression.predict([min_x])[0][0])
      self.stop = (max_x[0], self.regression.predict([max_x])[0][0])

  
  def __calculate_distance(self, x, y):
    if self.slope == 0:
        return abs(y - (self.slope * x + self.b))
    # elif self.slope == float('inf'):
    #   return abs(x - )
    perp_slope = -1 / self.slope
    perp_b = (y - perp_slope * x)
    intersect_x = (b - perp_b) / (perp_slope - self.slope)
    intersect_y = intersect_x * self.slope + self.b
    distance = math.sqrt((intersect_y-y)**2 + (intersect_x-x)**2)
    return distance

  def nearest_point_and_distance(self, pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)
  
  def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z

  def length(v):
      x,y,z = v
      return math.sqrt(x*x + y*y + z*z)

  def vector(b,e):
      x,y,z = b
      X,Y,Z = e
      return (X-x, Y-y, Z-z)

  def unit(v):
      x,y,z = v
      mag = length(v)
      return (x/mag, y/mag, z/mag)

  def distance(p0,p1):
      return length(vector(p0,p1))

  def scale(v,sc):
      x,y,z = v
      return (x * sc, y * sc, z * sc)

  def add(v,w):
      x,y,z = v
      X,Y,Z = w
      return (x+X, y+Y, z+Z)

  def draw_wall(self, screen, x_min, x_max, y_min, y_max):
    screen_width = x_max - x_min
    screen_height = y_max - y_min

    x_add_num = -1 * self.min[0]
    x_scale = screen_width / (self.max[0] - self.min[0])

    y_add_num = -1 * self.min[1]
    y_scale = screen_height / (self.max[1] - self.min[1])

    x_start = self.min[0]
    y_start = self.min[1]
    
    x_stop = self.max[0]
    y_stop = self.max[1]

    x_start += x_add_num
    x_stop += x_add_num
    x_start *= x_scale
    x_stop *= x_scale

    y_start += y_add_num
    y_stop += y_add_num
    y_start *= y_scale
    y_stop *= y_scale

    x_start = int(x_start)
    x_stop = int(x_stop)
    y_start = int(y_start)
    y_stop = int(y_stop)


    # self.logger.log("adding point", self.point[0], self.point[1], "on screen at", x, y)
    print("x_start type", type(x_start))

    pygame.draw.line(surface=screen, color=Colors.BLUE, start_pos=(x_start, y_start), end_pos=(x_stop, y_stop), width=8)

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

    # test_wall = Wall()
    # test_wall.add_point(0, 0)
    # test_wall.add_point(10, 10, update_regression=True)
    # self.walls.add(test_wall)
    # self.count_since_last_refresh = 0
  
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
    
    # if self.count_since_last_refresh > 10:
      self.refresh_walls()
    #   self.count_since_last_refresh = 0
    # else:
    #   self.count_since_last_refresh += 1
      
  def refresh_walls(self):
    pass

  def print_map(self):
    for row in self.map:
      self.logger.log(row)
  
  def draw_map(self, screen, x_min, x_max, y_min, y_max):
    #parameters are given as actual dimensions, not from 0 to 1
    print("draw_map called with", x_min, x_max, y_min, y_max)
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

    if y_scale > x_scale:
      self.logger.log("adjusting y_scale")
      y_screen_adjustment = (screen_height - screen_width) / 2
      x_screen_adjustment = 0
      y_scale = x_scale
    else:
      self.logger.log("adjusting x_scale")
      #scale_ratio = (x_scale - y_scale) / 2
      x_screen_adjustment = (screen_width - screen_height) / 2
      y_screen_adjustment = 0
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
      self.logger.log("adding point", point[0], point[1], "on x, y  at", x, y)
      pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=10)
    # for wall in self.walls:
    #   self.logger.log("start, stop of wall", wall.start, wall.stop)
    #   wall.draw_wall(screen=screen, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)