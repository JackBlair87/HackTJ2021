from .Communicator import Communicator
from .InfoPacket import InfoPacket
from .WallMap import WallMap
from .GroundStation import Mode

from math import pi

class Robot:
    ENCODER_COUNTS_PER_REVOLUTION = 20
    WHEEL_RADIUS = 5
    WHEEL_CIRCUMFERENCE = pi * WHEEL_RADIUS ** 2
    WHEEL_INCHES_PER_COUNT = WHEEL_CIRCUMFERENCE / ENCODER_COUNTS_PER_REVOLUTION
  
    def __init__(self, x = 0.0, y = 0.0, angle = pi/2):
        self.left_encoder_counts = 0
        self.right_encoder_counts = 0
        self.coordinates = [x, y]
        self.angle = angle
        self.dataPackets = []
        self.communicator = Communicator()
        self.communicator.initiate_bluetooth()
        self.mode = Mode.stop
        
    def add_data(self, InfoPacket):
        self.dataPackets.append(InfoPacket)
        
    def deactivate_robot(self):
        self.communicator.deactivate_bluetooth()
        
    def update_location(self):
        if(self.dataPackets[-1] != None and self.dataPackets[-2] != None): #If there are two data packets
            differenceR = self.dataPackets[-1].right_encoder_counts - self.dataPackets[-2].right_encoder_counts #Find the difference between last transmittion
            differenceL = self.dataPackets[-1].left_encoder_counts - self.dataPackets[-2].left_encoder_counts
            if(self.dataPackets[-1].state != 0, 1, 2): #Or the difference between last angle if rotation
                deltaAngle = self.dataPackets[-1].rotation - self.dataPackets[-2].rotation
                
    
            