from Communicator import Communicator
import math
from math import pi
import numpy
import pygame
import sys
from Resources import Mode, State, InfoPacket, WheelInfo, Logger

class Robot:
    def __init__(self, image, x = 0.0, y = 0.0, angle = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.convert_alpha()
        self.size = self.image.get_size()
        self.left_encoder_counts = 0
        self.right_encoder_counts = 0
        self.xcoord = x - self.size[0]/2
        self.ycoord = y - self.size[1]/2
        self.angle = angle
        self.dataPackets = [InfoPacket(angle=90), InfoPacket(angle=90)]
        self.communicator = Communicator(enabled = False)
        self.communicator.initiate_bluetooth()
        self.state = State.stop
        self.communicator.transmit_info(self.state)
        # self.logger = Logger()
        
    def add_data(self):
        new_packet = self.communicator.recieve_info(self.state)
        if new_packet != None:
            self.dataPackets.append(new_packet)
            self.__update_location()
            print(self.dataPackets[-1])
            # logger.log(new_packet)
        
    def deactivate_robot(self):
        self.communicator.deactivate_bluetooth()
        
    def change_state(self, new_state = State.stop):
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
        screen.blit(pygame.transform.rotate(self.image, self.angle), (self.xcoord + (width/2), self.ycoord + (height/2)))
        
    def __update_location(self):
        delta_x, delta_y, angle = self.__calculate_delta_location_change()
        print("delta_x, delta_y, delta_angle:", delta_x, delta_y, angle)
        self.xcoord += delta_x
        self.ycoord += delta_y
        self.angle = angle

    def __calculate_delta_location_change(self):
        differenceR = self.dataPackets[-1].right_encoder_counts - self.dataPackets[-2].right_encoder_counts #Find the difference between last transmittion
        differenceL = self.dataPackets[-1].left_encoder_counts - self.dataPackets[-2].left_encoder_counts
        difference_average = (differenceL + differenceR) / 2
        if self.dataPackets[-1].state == State.turn_left or self.dataPackets[-1].state == State.turn_right: #Or the difference between last angle if rotation
            delta_x = 0
            delta_y = 0
            angle = self.dataPackets[-1].rotation
        elif self.dataPackets[-1].state == State.forward or self.dataPackets[-1].state == State.reverse:
            delta_r_cm = difference_average * WheelInfo.WHEEL_CM_PER_COUNT
            angle = self.dataPackets[-1].rotation
            
            #if it's going reverse, calculate it like it's going forward backward
            if self.dataPackets[-1].state == State.reverse:
                angle + 180
            
            print("angle:", angle)
            angle_radians = math.radians(angle)
            print("angle_radians:", angle_radians)

            #if we adjusted the angle value bc we're going backward, undo that when we return delta_angle
            if self.dataPackets[-1].state == State.reverse:
                angle - 180
            
            #transform the data with the angle
            delta_x = delta_r_cm * math.cos(math.radians(angle))
            delta_y = delta_r_cm * math.sin(math.radians(angle))
        else:
            delta_x = 0
            delta_y = 0
            angle = 0

        return delta_x, delta_y, angle
        
    def sweep(self):
        pass
         #self.dataPackets[-1].front_distance
    #move forward
    #while front is clear and wall to
    #move forward

    def get_state_from_encoder(self, r, l):
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