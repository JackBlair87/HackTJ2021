import serial
import time
import sys
from Resources import InfoPacket, Logger
import threading

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600, enabled = True):
    self.port = port
    self.baud = baud
    self.bluetooth = None
    self.enabled = enabled
    self.connected = False
    
    self.logger = Logger("Communicator")
    if self.enabled:
        try:
          self.initiate_bluetooth()
        except:
          self.logger.log("Communicator: bluetooth not connected")
          self.logger.log(sys.exc_info())
          
  def initiate_bluetooth(self):
    if self.enabled:
      self.bluetooth = serial.Serial(self.port, self.baud, timeout=0) #Start communications with the bluetooth unit
      self.bluetooth.flushInput() #This gives the bluetooth a little kick
      self.connected = True
    
#Timestamp 12321, State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self, old_state = 0):
    if not (self.enabled and self.connected):
      return None
    
    input_data = self.bluetooth.readline().decode()
    if(input_data == None or input_data == ""):
      return None
    
    print("Data ----------", input_data)
      #   #incoming data is separated with commas and represents these values in order: Millis, state, front distance, right distance, left encoder total, right encoder total, angle total
    newdata = input_data.split(",")
    #strip each value
    #add the list of new values to the old list
    #check if value isn't empty
    #check for complete data packet
      #remove them from the list
      #make a new data packet
      
    newdata[-1] = newdata[-1].strip()
    self.logger.logDataPacket(input_data)
    if len(newdata) < 7:
      self.logger.log("^New data list is less than 7^")
      #self.connected = False
      return None
    
    if(old_state != 0 and newdata[0] == 0):
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], True)
    else:
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], False)
      self.connected = True
      return info
    #else:
      #return None
    
  def transmit_info(self, state = 0):
    if self.enabled and self.connected:
      self.previousState = state
      #self.bluetooth.flushInput()
      self.bluetooth.write(str.encode(str(state))) #These need to be bytes not unicode, plus a number
    
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