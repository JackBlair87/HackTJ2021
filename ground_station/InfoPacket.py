class InfoPacket:
  def __init__(self, time = 0, state = 0, f_distance = 0, r_distance = 0, l_encoderCounts = 0, r_encoderCounts = 0, angle = 0, e_stopped = False):
    self.state = int(state)
    self.time = float(time)/1000
    self.right_distance = float(r_distance)
    self.front_distance = float(f_distance)
    self.left_encoder_counts = int(l_encoderCounts)
    self.right_encoder_counts = int(r_encoderCounts)
    self.rotation = float(angle)
    self.emergency_stopped = e_stopped
    # if e_stopped.lower() == "false":
    #   self.emergency_stopped = False
    # elif e_stopped.lower() == "true":
    #   self.emergency_stopped = True    
    # else:
    #   print("Error converting e_stopped to boolean in class InfoPacket")
    
  def __str__(self):
    return "Time Stamp: " + str(self.time) + ", Current State: " + str(self.state) + ", Forward Distance: " + str(self.front_distance) + ", Right Distance: " + str(self.right_distance) + ", Total Left Encoder Movement: " + str(self.left_encoder_counts) + ", Total Right Encoder Movement: " + str(self.right_encoder_counts) + ", Rotation Angle: " + str(self.rotation) + ", Emergency Stopped: " + str(self.emergency_stopped)