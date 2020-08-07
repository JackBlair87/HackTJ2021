from Communicator import Communicator
import math
from math import pi
import pygame
import sys
import time
from Resources import Mode, State, InfoPacket, WheelInfo, Logger, Rectifier

class Robot:
    def __init__(self, image, x = 0.0, y = 0.0, angle = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.convert_alpha()
        self.size = self.image.get_size()
        self.left_encoder_counts = 0
        self.right_encoder_counts = 0
        self.location = (x - self.size[0]/2, y - self.size[1]/2)
        #^separate things above here into just the draw_robot method
        self.angle = angle
        self.dataPackets = [InfoPacket(angle=90), InfoPacket(angle=90)] #angles here should be changed to 0?
        self.communicator = Communicator(enabled = True)
        self.communicator.initiate_bluetooth()
        self.state = State.stop
        self.communicator.transmit_info(self.state)
        self.logger = Logger("Robot")
        self.max_dist = 150
        self.last_index = -1
        self.rectifier = None
        self.last_state_switch_time = int(round(time.time() * 1000))
        
    def add_data(self):
        new_packet = self.communicator.recieve_info(self.state)
        if new_packet != None:
            self.dataPackets.append(new_packet)
            self._update_location()
            self.logger.log(self.dataPackets[-1])
            self.logger.log('adding data to robot')
            return self.generate_points() #returns two points
        
    def quitProgram(self):
        self.communicator.transmit_info(State.stop)
        self.communicator.deactivate_bluetooth()

    # def draw_robot(self, screen, x_min, x_max, y_min, y_max):
    #     #parameters are given as actual dimensions, not from 0 to 1
    #     width = x_max - x_min
    #     height = y_max - y_min
    #     screen.blit(pygame.transform.rotate(self.image, self.angle), (self.location[0] + (width/2) + x_min, self.location[1] + (height/2) + y_min))
        
    def _update_location(self):
        if self.rectifier is None and len(self.dataPackets) >= 3: # when we get the first new data, initialize
            last_packet = self.dataPackets[-1]
            self.rectifier = Rectifier(start_angle=last_packet.rotation, start_l_encoder=last_packet.left_encoder_counts, start_r_encoder=last_packet.right_encoder_counts)
        

        last_packet = self.dataPackets[-1]
        last_packet.rotation = self.rectifier.offset_angle(last_packet.rotation)
        last_packet.left_encoder_counts = self.rectifier.offset_l_encoder(last_packet.left_encoder_counts)
        last_packet.right_encoder_counts = self.rectifier.offset_r_encoder(last_packet.right_encoder_counts)

        delta_x, delta_y, angle = self._calculate_delta_location_change()
        self.logger.log("delta_x, delta_y, delta_angle:", delta_x, delta_y, angle)
        self.location = (self.location[0] + delta_x, self.location[1] + delta_y)
        self.logger.log('new position:', self.location[0], self.location[1], self.angle)

    def _calculate_delta_location_change(self):
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
            
            self.logger.log("angle: " + str(angle))
            angle_radians = math.radians(angle)
            self.logger.log("angle_radians: " + str(angle_radians))

            #if we adjusted the angle value bc we're going backward, undo that when we return delta_angle
            if self.dataPackets[-1].state == State.reverse:
                angle - 180
            
            #transform the data with the angle
            delta_x = delta_r_cm * math.cos(math.radians(angle))
            delta_y = delta_r_cm * math.sin(math.radians(angle))
        else:
            delta_x = 0
            delta_y = 0
            #angle = 0
            angle = self.dataPackets[-1].rotation #experimental

        return delta_x, delta_y, angle
        
    def generate_points(self):
        if self.dataPackets[-1] != None:
            distForward = self.dataPackets[-1].front_distance #in cm
            distRight = self.dataPackets[-1].right_distance #in cm
            
            if distForward >= 0 and distForward < self.max_dist and distRight >= 0 and distRight < self.max_dist:
                forward = (distForward * math.cos(math.radians(self.angle)), distForward * math.sin(math.radians(self.angle)))
                right = (distRight * math.cos(math.radians(self.angle-90)), distRight * math.sin(math.radians(self.angle-90)))
                return (forward, right)
            elif distForward >= 0 and distForward < self.max_dist:
                return ((distForward * math.cos(math.radians(self.angle)), distForward * math.sin(math.radians(self.angle))))
            elif distRight >= 0 and distRight < self.max_dist:
                return ((distRight * math.cos(math.radians(self.angle-90)), distRight * math.sin(math.radians(self.angle-90))))
            else:
                return ()
        
    

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
        # self.logger.log("Rahel needs to work on this method BIG SMH")
        return self.dataPackets[-1].front_distance > 20

    def right_is_clear(self):
        return self.dataPackets[-1].right_distance > 20

    def change_state(self, new_state = State.stop):
        self.state = new_state
        self.communicator.transmit_info(self.state)
        self.logger.log("State changed to: " + State.all_states[self.state])

    def sweep(self):
        self.logger.log("sweep method")
        if int(round(time.time() * 1000)) - self.last_state_switch_time > 250:
            self.logger.log("sweep method testing")
            self.last_state_switch_time = int(round(time.time() * 1000))
            if self.front_is_clear():
                self.state = State.forward
            else:
                self.state = State.turn_right

        self.communicator.transmit_info(self.state)
        self.logger.log("State changed to: " + State.all_states[self.state])