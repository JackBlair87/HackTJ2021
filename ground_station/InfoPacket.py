class InfoPacket:
  def __init__(self, informationstate = None, f_distance = None, r_distance = None, l_encoderCounts = None, r_encoderCounts = None, angle = None, e_stopped = True):
    self.state = state
    self.right_distance = r_distance
    self.front_distance = f_distance
    self.left_encoder_counts = l_encoderCounts
    self.right_encoder_counts = r_encoderCounts
    self.rotation = angle
    self.emergency_stopped = e_stopped
    
  def __str__(self):
    return "Current State: " + self.state + ", Forward Distance: " + self.front_distance + ", Right Distance: " + self.right_distance + ", Total Left Encoder Movement: " + self.left_encoder_counts + ", Total Right Encoder Movement: " + self.right_encoder_counts + ", Rotation Angle" + self.rotation + ", Emergency Stopped?" + self.emergency_stopped