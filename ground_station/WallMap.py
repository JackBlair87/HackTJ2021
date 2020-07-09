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
  def __init__(self):
    self.regression = LinearRegression()
    self.slope = None #these 
    self.b = None
    self.x_points = []
    self.y_points = []
    self.min_x = float('inf')
    self.max_x = -float('inf')
    self.min_y = float('inf')
    self.max_y = -float('inf')

    
  def add_point(self, x, y, update_regression=False):
    self.x_points.append([x])
    self.y_points.append([y])
    if update_regression:
      self.update_regression()
  
  def update_regression(self, x_train, y_train):
    x_train = [[elem] for elem in x_train]
    y_train = [[elem] for elem in y_train]
    self.x_points.extend(x_train)
    self.y_points.extend(y_train)

    self.regression.fit(self.x_points, self.y_points)
    slope = round(self.regression.coef_[0][0], 4)
    new_x_min = min(x_train)
    new_x_max = max(x_train)
    new_y_min = min(y_train)
    new_y_max = max(y_train)
    if slope > 100:
      self.slope = float('inf')
      self.b = None
      if new_y_max > self.max_y:
        self.max_y = new_y_max
      if new_y_min < self.min_y:
        self.min_y = new_y_min
    else:
      self.slope = slope
      self.b = round(self.regression.intercept_[0], 4)
      if new_x_max > self.max_x:
        self.max_x = new_x_max
      if new_x_min < self.min_x:
        self.min_x = new_x_min
  

  
  def calculate_distance(x, y):
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
    self.x_min = -10
    self.x_max = 10
    self.y_min = -10
    self.y_max = 10
  
  def add_obstacle_point(self, x, y):
    self.logger.log("adding point (" + str(x) + ', ' + str(y))
    self.obstacle_points.add((x, y))
    if x > self.x_max - 10:
      self.x_max = x + 10
    if x < self.x_min + 10:
      self.x_min = x - 10
    
    if y > self.y_max - 10:
      self.y_max = y + 10
    if y < self.y_min + 10:
      self.y_min = y - 10
      
  def print_map(self):
    for row in self.map:
      self.logger.log(row)
  
  def draw_map(self, screen, x_min, x_max, y_min, y_max):
    #parameters are given as actual dimensions, not from 0 to 1
    width = x_max - x_min
    height = y_max - y_min


    map_width = self.x_max - self.x_min
    p_width_map = self.x_max - 0
    n_width_map = 0 - self.x_min
    p_width_screen = width * p_width_map / map_width
    n_width_screen = width * n_width_map / map_width
    width_start_screen = x_max - p_width_screen
    p_width_scale = p_width_screen / p_width_map
    n_width_scale = p_width_screen / n_width_map

    map_height = self.y_max - self.y_min
    p_height_map = self.y_max - 0
    n_height_map = 0 - self.y_min
    p_height_screen = height * p_height_map / map_height
    n_height_screen = height * n_height_map / map_height
    height_start_screen = y_max - p_height_screen
    p_height_scale = p_height_screen / p_height_map
    n_height_scale = p_height_screen / n_height_map

    # x_scale = width / (self.x_max - self.x_min)
    # y_scale = height / (self.y_max - self.y_min)
    # if x_scale > y_scale:
    #   x_scale = y_scale
    # else:
    #   y_scale = x_scale
    self.logger.log("x bounds:", x_min, x_max)
    self.logger.log("y bounds:", y_min, y_max)
    self.logger.log("self.x bounds", self.x_min, self.x_max)
    self.logger.log("self.y bounds", self.y_min, self.y_max)
    for point in self.obstacle_points:
      # center = (point[0] * x_scale, point[1] * y_scale)
      x = point[0]
      y = point[1]
      if x > 0:
        x = x * p_width_scale + width_start_screen
      else:
        x = x * n_width_scale + width_start_screen
      
      if y > 0:
        y = y * p_height_scale + height_start_screen
      else:
        y = y * n_height_scale + height_start_screen
      center = (x, y_max - y) #correct the order (x, y) to (r, c)
      self.logger.log("adding point", point[0], point[1], "on screen at", center[0], center[1])
      # print("scaled center:", center)
      pygame.draw.circle(surface=screen, color=Colors.BLUE, center=center, radius=10)