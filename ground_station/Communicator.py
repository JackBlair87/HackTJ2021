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
    self.time_packet = [time.time()]
    self.data_stream = ""
    
    self.logger = Logger("Communicator")
    if self.enabled:
      try:
        self.initiate_bluetooth()
      except:
        self.logger.log("Communicator: Bluetooth Not Connected")
        self.logger.log(sys.exc_info())
          
  def initiate_bluetooth(self):
    if self.enabled:
      self.bluetooth = serial.Serial(self.port, self.baud, timeout=0) #Start communications with the bluetooth unit
      self.bluetooth.flushInput() #This gives the bluetooth a little kick
      self.connected = False
    
#Timestamp 12321, State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self, old_state = 0):
    if not (self.enabled):
      return None
    
    try:
      input_data = self.bluetooth.readline().decode()
    except:
      print('bluetooth is not connected, error in receive_info method')
      self.logger.log(sys.exc_info())
      return None
    #self.logger.logDataPacket('input_data:', input_data)
    if(input_data == None or input_data.strip() == ""):
      return None
    
    self.data_stream += input_data.strip()
    
    while self.data_stream.strip() != "":
      if self.data_stream[0] == ":": #If first character is a colon
        if self.data_stream.count(":") >= 2:
          self.data_stream = self.data_stream[1:]
          data_packet_list = self.data_stream[0:self.data_stream.index(":")]
          self.data_stream = self.data_stream[len(data_packet_list) + 1:]
          return self.create_info_packet(data_packet_list.split(","))
        else:
          return None
      else:
        self.data_stream = self.data_stream[self.data_stream[self.data_stream.index(':')] : ]
        self.logger.log("self.data_stream", self.data_stream)
        print("first character is", int(self.data_stream[0]))
    
    return None
      #   #incoming data is separated with commas and represents these values in order: Millis, state, front distance, right distance, left encoder total, right encoder total, angle total
   
  def create_info_packet(self, data):
    print("data:", data)
    newdata = []
    for element in data:
      newdata.append(element.strip())
    self.time_packet.append(time.time() * 1000)
    # print(newdata)
    # self.logger.logDataPacket(newdata)
    self.connected = True
    
    return InfoPacket(newdata[0], newdata[1], newdata[2], newdata[3], newdata[4], newdata[5])
      
  def transmit_info(self, state = 0):
    self.connection_check(500)
    if self.enabled:
      self.previousState = state
      try:
        self.bluetooth.write(str.encode(str(state))) #These need to be bytes not unicode, plus a number
      except:
        print('error transmitting info, bluetooth was disconnected from transmit_info method')
        self.logger.log(sys.exc_info())
        
  def deactivate_bluetooth(self):
    if self.enabled:
      self.bluetooth.close()
      
  def connection_check(self, benchmark):
    if self.enabled:
      if len(self.time_packet) == 0:
        self.connected = False
      
      if (time.time() * 1000) - self.time_packet[-1] > benchmark:
        self.connected = False
    
#Ideal Use
#c = Communicator()
#c.initiate_bluetooth()
#while(True):
  #c.transmit_info(robot.state)
  #robot.addInfo(c.recieve_info())
#c.deactivate_bluetooth()