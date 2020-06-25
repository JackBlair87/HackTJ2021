import serial
import time
from .InfoPacket import InfoPacket

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600):
    self.port = port
    self.baud = baud
    self.bluetooth = None
    self.initiate_bluetooth()
    
  def initiate_bluetooth(self):
    self.bluetooth = serial.Serial(self.port, self.baud) #Start communications with the bluetooth unit
    self.bluetooth.flushInput() #This gives the bluetooth a little kick
    
#State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self, old_state = 0):
    input_data = self.bluetooth.readline().decode() #This reads the incoming data
    #incoming data is separated with commas and represents these values in order: Millis, state, front distance, right distance, left encoder total, right encoder total, angle total
    newdata = input_data.split(",")
    print(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6])
    if(self.previousState != 0 and newdata[0] == 0):
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], True)
    else:
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], False)
    return info
  
  def transmit_info(self, state = 0):
    self.previousState = state
    self.bluetooth.write(str.encode(str(state))) #These need to be bytes not unicode, plus a number
    
  def deactivate_bluetooth(self):
    self.bluetooth.close()
    
    
#Ideal Use
#c = Communicator()
#c.initiate_bluetooth()
#while(True):
  #c.transmit_info(robot.state)
  #robot.addInfo(c.recieve_info())
#c.deactivate_bluetooth()