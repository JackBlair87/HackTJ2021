import serial
import time
from InfoPacket import InfoPacket

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600):
    self.port = port
    self.baud = baud
    self.bluetooth = None
    self.initiate_bluetooth()
    
  def initiate_bluetooth(self):
    pass
    
#Timestamp 12321, State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self, old_state = 0):
    pass
  
  def transmit_info(self, state = 0):
    print("Transimiting state:", state)
    
  def deactivate_bluetooth(self):
    pass