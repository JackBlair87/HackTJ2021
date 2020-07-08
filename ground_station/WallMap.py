from Resources import Logger, Colors
import pygame

class WallMapOld:
  """
  todo: Think about using an auxilary set to hold raw data points. Whenever possible,
  calculate a regression and the regression lines to another set with regressions. This would mean more processing
  upfront, but it would save a lot of memory.
  The line regression would have the regression, as well as the start and and and coordinates.
  """
  UNEXPLORED = -1
  NO_OBSTACLE = 0
  OBSTACLE = 1
  def __init__(self, matrix=None):
    self.logger = Logger("WallMap")
    if matrix is not None:
      self.map = matrix
    else:
      self.map = [[WallMap.UNEXPLORED, WallMap.UNEXPLORED, WallMap.UNEXPLORED],
                  [WallMap.UNEXPLORED, WallMap.UNEXPLORED, WallMap.UNEXPLORED],
                  [WallMap.UNEXPLORED, WallMap.UNEXPLORED, WallMap.UNEXPLORED]]
  
  def update_map(location, new_data):
    pass
  def add_wall(self, point, count=1):
    r = point[0]
    c = point[1]

    #ensure that the map is a square
    self.add_rows(r - len(self.map))
    self.add_columns(c - len(self.map[0]))
    self.map[r][c] += 1
    
  def add_rows(self, row_count):
    if row_count < 0:
      return False
    self.map.reverse()
    for i in range(row_count):
      self.map.append([0 for x in range(len(self.map[0]))])
    self.map.reverse()
    return True
  
  def add_columns_right(self, col_count):
    if col_count < 0:
      return False
    for row in self.map:
      row.append(WallMap.UNEXPLORED)
      
  def add_columns_left(self, col_count):
    if col_count < 0:
      return False
    for row in self.map:
      row.insert(0, WallMap.UNEXPLORED)
      
  def print_map(self):
    for row in self.map:
      self.logger.log(row)
  

class Wall:
  def __init__(self, regression=None, x_train=None, y_train=None):
    if x_train is not None and y_train is not None:
      self.calculate_regression(x_train, y_train)
    else:
      self.regression = LinearRegression()
      self.slope = None
      self.b = None
  
  def calculate_regression(self, x_train, y_train):
    x_train = [[elem] for elem in x_train]
    y_train = [[elem] for elem in y_train]
    
    self.regression.fit(x_train, y_train)
    self.slope = self.regression.coef_[0][0]
    self.b = self.regression.intercept_[0]
  
  def calculate_distance(x, y):
    if self.slope == 0:
        return y - (self.slope * x + self.b)
    perp_slope = -1 / self.slope
    perp_b = (y - perp_slope * x)
    intersect_x = (b - perp_b) / (perp_slope - self.slope)
    intersect_y = intersect_x * self.slope + self.b
    distance = math.sqrt((intersect_y-y)**2 + (intersect_x-x)**2)
    return distance

  def y_prediction(x):
    regressor.predict(x)

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
  
  def add_obstacle_point(self, x, y):
    pass
      
  def print_map(self):
    for row in self.map:
      self.logger.log(row)
  
  def draw_map(self, screen, x_min, x_max, y_min, y_max):
    #parameters are given as actual dimensions, not from 0 to 1
    width = x_max - x_min
    height = y_max - y_min
    center = (x_min + width / 2, y_min + height / 2)
    pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=50)