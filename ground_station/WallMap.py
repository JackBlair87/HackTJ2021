class WallMap:
  UNEXPLORED = -1
  NO_OBSTACLE = 0
  OBSTACLE = 1
  def __init__(self, matrix=None):
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
      print(row)
  