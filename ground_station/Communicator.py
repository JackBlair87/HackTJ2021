class Communicator:
  def __init__(self, l_stop=90, r_stop=90):
    self.l_stop_power = l_stop
    self.r_stop_power = r_stop
  def get_data(self):
    #return new data if any, otherwise return None
    return None
  def set_servos(self, l_power, r_power):
    pass
  def stop_all(self):
    self.set_servos(self.l_stop_power, self.r_stop_power)