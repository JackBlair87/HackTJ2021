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
    self.data_stream = ""
    
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
    
    self.data_stream += input_data
    
    if self.data_stream.count(":") >= 2:
      #print(self.data_stream)
      self.data_stream = self.data_stream.lstrip()
      self.data_stream = self.data_stream[1:]
      data_packet = self.data_stream[0 : self.data_stream.index(":") + 1]
      data_packet = data_packet[:-1]
      #print(data_packet)
      self.data_stream = self.data_stream[len(data_packet) + 1: ]
      self.data_stream = self.data_stream.lstrip()
      data_packet = data_packet.split(",")
      return self.create_info_packet(data_packet, old_state)
    
    # if len(self.data_stream) == 7:
    #   data = self.create_info_packet(self.data_stream, old_state)
    #   if data != None:
    #     self.data_stream = []
    #     return data
    
      #   #incoming data is separated with commas and represents these values in order: Millis, state, front distance, right distance, left encoder total, right encoder total, angle total
   
  def create_info_packet(self, data, old_state):
    print(data)
    newdata = []
    for element in data:
      newdata.append(element.strip())
    
    print(newdata)
    self.logger.logDataPacket(newdata)
    
    if(old_state != 0 and newdata[0] == 0):
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], True)
    else:
      info = InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5], newdata[6], False)
      self.connected = True
      return info
      
  def transmit_info(self, state = 0):
    if self.enabled and self.connected:
      self.previousState = state
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