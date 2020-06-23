class InfoPacket:
  def __init__(self, state = 0, f_distance = 0, r_distance = 0, l_encoderCounts = 0, r_encoderCounts = 0, e_stopped = False):
    self.state = state
    self.right_distance = r_distance
    self.front_distance = f_distance
    self.left_encoder_counts = l_encoderCounts
    self.right_encoder_counts = r_encoderCounts
    self.emergency_stopped = e_stopped
    
  