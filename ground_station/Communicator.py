#/dev/tty.HC-05-DevB
import serial
import time

class Communicator:
  def __init__(self, port = "/dev/tty.HC-05-DevB", baud = 9600):
    self.port = port
    self.baud = baud
    
  def start_test(self):
    print("Start")
    bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput() #This gives the bluetooth a little kick
    for i in range(500): #send 5 groups of data to the bluetooth
	    print("Ping")
	    bluetooth.write(b"BOOP "+str.encode(str(i)))#These need to be bytes not unicode, plus a number
	    input_data=bluetooth.readline() #This reads the incoming data
	    print(input_data.decode())#These are bytes coming in so a decode is needed
	    time.sleep(0.1) #A pause between bursts
    bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob