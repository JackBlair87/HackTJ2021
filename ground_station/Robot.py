from Communicator import Communicator
from InfoPacket import InfoPacket
#from WallMap import WallMap
from GroundStation import Mode, State

from math import pi

class Robot:
    ENCODER_COUNTS_PER_REVOLUTION = 20
    WHEEL_RADIUS = 5 #in cm
    WHEEL_CIRCUMFERENCE = pi * WHEEL_RADIUS ** 2
    WHEEL_CM_PER_COUNT = WHEEL_CIRCUMFERENCE / ENCODER_COUNTS_PER_REVOLUTION
  
    def __init__(self, x = 0.0, y = 0.0, angle = 0):
        self.left_encoder_counts = 0
        self.right_encoder_counts = 0
        self.xcoord = x
        self.ycoord = y
        self.angle = angle
        self.dataPackets = []
        self.communicator = Communicator(None, None, False)
        self.communicator.initiate_bluetooth()
        self.state = State.stop
        
    def add_data(self, infoPacket):
        self.dataPackets.append(infoPacket)
        self.update_location()
        
    def deactivate_robot(self):
        self.communicator.deactivate_bluetooth()
        
    def change_state(self, new_state = State.stop):
        if(new_state != self.state):
            self.state = new_state
            self.communicator.transmit_info(self.state)
        
    def update_location(self):
        if(self.dataPackets[-1] != None and self.dataPackets[-2] != None): #If there are two data packets
            differenceR = self.dataPackets[-1].right_encoder_counts - self.dataPackets[-2].right_encoder_counts #Find the difference between last transmittion
            differenceL = self.dataPackets[-1].left_encoder_counts - self.dataPackets[-2].left_encoder_counts
            if(self.dataPackets[-1].state != State.stop, State.forward, State.reverse): #Or the difference between last angle if rotation
                deltaAngle = self.dataPackets[-1].rotation - self.dataPackets[-2].rotation
    
    def sweep(self):
        print("Rahel needs to work on this method BIG SMH")
    #while front is clear and wall to right
    #   move forward
    #while front is clear and wall to 
    #   move forward

    def if_front_clear(self):
        print("Rahel needs to work on this method BIG SMH")
        
#self.state = State.forward