from Communicator import Communicator
from InfoPacket import InfoPacket
import math
from math import pi
import numpy
import pygame

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

    def __init__(self, image, x = 0.0, y = 0.0, angle = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.convert_alpha()
        self.size = self.image.get_size()
        self.left_encoder_counts = 0
        self.right_encoder_counts = 0
        self.xcoord = x - self.size[0]/2
        self.ycoord = y - self.size[1]/2
        self.angle = angle
        self.dataPackets = [InfoPacket(), InfoPacket()]
        self.communicator = Communicator(enabled = False)
        self.communicator.initiate_bluetooth()
        self.state = State.stop
        self.communicator.transmit_info(self.state)
        
    def add_data(self):
        new_packet = self.communicator.recieve_info(self.state)
        if new_packet != None:
            self.dataPackets.append(new_packet)
            self.__update_location()
            print(self.dataPackets[-1])
        
    def deactivate_robot(self):
        self.communicator.deactivate_bluetooth()
        
    def change_state(self, new_state = State.stop):
        if(new_state != self.state):
            self.state = new_state
            self.communicator.transmit_info(self.state)
            
    def draw_robot(self, screen, x_min, x_max, y_min, y_max, screen_height = 800, screen_width = 1440):
        #translates the 0-1 scale to the actual screen dimensions
        x_min = screen_width * x_min
        x_max = screen_width * x_max
        y_min = screen_height * y_min
        y_max = screen_height * y_max
        width = x_max - x_min
        height = y_max - y_min

        # robot_width, robot_height = ROBOT.get_size()
        # robot_height_to_width = robot_height/robot_width
        # robot_width = int(robot_width * .5)
        # robot_height = robot_width * robot_height_to_width
        # print(self.xcoord, self.ycoord)
        screen.blit(self.image, (self.xcoord + (width/2), self.ycoord + (height/2)))
        
    def __update_location(self):
        print("update_location")
        delta_x, delta_y, delta_angle = calculate_delta_location_change()
        print("delta_x, delta_y, delta_angle:", delta_x, delta_y, delta_angle)
        self.xcoord += delta_x
        self.ycoord += delta_y
        self.angle += delta_angle

    def __calculate_delta_location_change(self):
        global WHEEL_CM_PER_COUNT
        differenceR = self.dataPackets[-1].right_encoder_counts - self.dataPackets[-2].right_encoder_counts #Find the difference between last transmittion
        differenceL = self.dataPackets[-1].left_encoder_counts - self.dataPackets[-2].left_encoder_counts
        difference_average = (differenceL + differenceR) / 2
        if self.dataPackets[-1].state == State.turn_left or self.dataPackets[-1].state == State.turn_right: #Or the difference between last angle if rotation
            delta_angle = self.dataPackets[-1].rotation - self.dataPackets[-2].rotation
        elif self.dataPackets[-1].state == State.forward or self.dataPackets[-1].state == State.reverse:
            delta_r_cm = difference_average * WHEEL_CM_PER_COUNT
            delta_angle = self.dataPackets[-1].rotation - self.dataPackets[-2].rotation
            
            #if it's going reverse, calculate it like it's going forward backward
            if self.dataPackets[-1].state == State.reverse:
                delta_angle_radians + 180
            
            delta_angle_radians = math.radians(delta_angle)

            #if we adjusted the angle value bc we're going backward, undo that when we return delta_angle
            if self.dataPackets[-1].state == State.reverse:
                delta_angle_radians - 180
            
            #transform the data with the angle
            delta_x = delta_r_cm * math.cos(math.radians(delta_angle))
        else:
            delta_x = 0
            delta_y = 0
            delta_angle = 0

        return delta_x, delta_y, delta_angle
        
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
        
        
#self.state = State.forward