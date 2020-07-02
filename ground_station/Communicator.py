import serial
import time
import sys
from Resources import InfoPacket, Logger

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600, enabled = True):
    self.port = port
    self.baud = baud
    self.bluetooth = None
    self.enabled = enabled
    self.connected = False
    self.start_time = int(round(time.time() * 1000))
    self.last_communication_time = self.start_time
    self.next_communcation = None
    self.logger = Logger("Communicator")
    if self.enabled:
        try:
          self.initiate_bluetooth()
        except:
          self.logger.log("Communicator: bluetooth not connected")
          self.logger.log(sys.exc_info())
          
  def initiate_bluetooth(self):
    if self.enabled:
      self.bluetooth = serial.Serial(self.port, self.baud) #Start communications with the bluetooth unit
      self.bluetooth.flushInput() #This gives the bluetooth a little kick
      self.connected = True
    
#Timestamp 12321, State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self, old_state = 0):
    if self.enabled and self.connected:
      input_data = self.bluetooth.readline().decode() #This reads the incoming data
      if(input_data == None):
        return None
      
      #incoming data is separated with commas and represents these values in order: Millis, state, front distance, right distance, left encoder total, right encoder total, angle total
      newdata = input_data.split(",")
      newdata[-1] = newdata[-1].strip()
      self.logger.logDataPacket(newdata)
      if len(newdata) < 7:
        self.logger.log("^New data list is less than 7^")
        return None
      
      if(old_state != 0 and newdata[0] == 0):
        info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], True)
      else:
        info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], False)
      self.logger.log(str(info))
      return info
  
  def transmit_info(self, state = 0):
    if self.enabled and self.connected and int(round(time.time() * 1000)) - self.last_communication_time > 250 and self.next_communcation is not None:
      self.previousState = state
      self.bluetooth.write(str.encode(str(state))) #These need to be bytes not unicode, plus a number
      self.bluetooth.flushInput()
      self.logger.log("Changed State to", self.next_communication)
      self.next_communication = None
      self.last_communication_time = int(round(time.time() * 1000)) - self.last_communication_time > 250
    else:
      self.next_communication = state
    
  def deactivate_bluetooth(self):
    if self.enabled and self.connected:
      self.bluetooth.close()
    
    
#Ideal Use
#c = Communicator()
#c.initiate_bluetooth()
#while(True):
  #c.transmit_info(robot.state)
  #robot.addInfo(c.recieve_info())
#c.deactivate_bluetooth()