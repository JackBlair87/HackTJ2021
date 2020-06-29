from Communicator import Communicator
from InfoPacket import InfoPacket
import math
from math import pi
import numpy


class Mode(): 
  stop = 0
  explore = 1
  sweep = 2
  manual = 3
  emergency_stop = 4
  #a list for easier debugging
  all_modes = ['Stop', 'Explore', 'Sweep', 'Manual', 'Emergency_stop']
  all_modes_english = ['Stopped', 'Exploring', 'Sweeping', 'Manual', 'Emergency Stopped']
  
class State():
  stop = 0
  forward = 1
  reverse = 2
  turn_left = 3
  turn_right = 4
  error = -1
  all_states = ['stop', 'forward', 'reverse', 'turn_left', 'turn_right', 'error']
  all_states_english = ['Stopped', 'Advancing', 'Reversing', 'Turning Left', 'Turning Right', 'Erroring']


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
        self.communicator = Communicator(enabled = False)
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
        if(self.dataPackets[-1] == None or self.dataPackets[-2] == None): #If there are two data packets
            return False
        differenceR = self.dataPackets[-1].right_encoder_counts - self.dataPackets[-2].right_encoder_counts #Find the difference between last transmittion
        differenceL = self.dataPackets[-1].left_encoder_counts - self.dataPackets[-2].left_encoder_counts
        if(self.dataPackets[-1].state != State.stop, State.forward, State.reverse): #Or the difference between last angle if rotation
            deltaAngle = self.dataPackets[-1].rotation - self.dataPackets[-2].rotation  
        
        calculated_state = get_state_from_encoder(differenceR, differenceL)
        if calculated_state == State.forward:
            # total_distance = 
            xcoord += d*numpy.cos(deltaAngle*pi/180)
            ycoord += d*numpy.sin(deltaAngle*pi/180)
        elif calculated_state == State.turn_left:
            pass
        elif calculated_state == State.turn_right:
            pass
        elif calculated_state == State.reverse:
            pass

    def sweep(self):
        pass
         #self.dataPackets[-1].front_distance
    #move forward
    #while front is clear and wall to
    #move forward

    def get_state_from_encoder(r, l):
        difference = r-l
        if math.abs(difference) < 2:
            if r > 0 and l > 0:
                return State.forward
            else:
                return State.reverse
        elif r > l:
            return State.turn_left
        elif l > r:
            return State.turn_right
        else:
            raise Exception("get_state_from_encoder method()")

    
    def front_is_clear(self):
        print("Rahel needs to work on this method BIG SMH")
        return self.dataPackets[-1].front_distance > 50

    def right_is_clear(self):
        return self.dataPackets[-1].right_distance > 50
    
    def average_encoder(self, l, r):
        return (l + r) / 2
        
        
#self.state = State.forward