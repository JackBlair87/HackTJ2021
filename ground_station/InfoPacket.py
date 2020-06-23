class InfoPacket:
  def __init__(self, r_distance=-1, f_distance=-1, l_encoderCounts=1, r_encoderCounts=0, e_stopped=True):
    self.right_distance = r_distance
    self.front_distance = f_distance
    self.left_encoder_counts = l_encoderCounts
    self.right_encoder_counts = r_encoderCounts
    self.emergency_stopped = e_stopped