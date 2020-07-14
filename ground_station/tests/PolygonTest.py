from shapely.geometry import Polygon, Point
import time


polygon = Polygon([(0, 0), (1, 0), (1, 1), (0,1)])

points = [(0, 0), (1, 0), (1, 1), (0,1)]

print(polygon.distance(Point(2, 2)))

print(len(list(polygon.exterior.coords)))
print(polygon.geom_type)

start_time = int(round(time.time() * 1000))
for i in range(100):
    polygon = Polygon(points)
print("time taken", int(round(time.time() * 1000)) - start_time)


"""

class WallOld:
  def __init__(self, points):
    self.regression = LinearRegression()
    self.slope = None #these 
    self.b = None
    self.x_points = []
    self.y_points = []
    self.min = (-float('inf'), -float('inf'))
    self.max = (float('inf'), float('inf'))
    self.logger = Logger("WallOld")
    if points is not None:
      for point in points:
        self.add_point(point[0], point[1])
      self.update_regression()

    
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
"""