#/dev/tty.HC-05-DevB
import serial
import time

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600):
    self.port = port
    self.baud = baud
    bluetooth=serial.Serial(self.port, self.baud) #Start communications with the bluetooth unit
    bluetooth.flushInput() #This gives the bluetooth a little kick
    
#State -1 to 4, Distance Sensor Front Double, Distance Sensor Right Double, Left Encoder Value Int, Right Encoder Value Int, Total Angle Double
  def recieve_info(self):
    print("Ping")
    bluetooth.write(b"BOOP "+str.encode(str(i)))#These need to be bytes not unicode, plus a number
    input_data=bluetooth.readline() #This reads the incoming data
    print(input_data.decode())#These are bytes coming in so a decode is needed
    time.sleep(0.1) #A pause between bursts
    bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob