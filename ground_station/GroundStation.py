from .Communicator import Communicator
from .WallMap import WallMap
from ui.BotDisplay import BotDisplay
import time
from math import pi

class GroundStation:
  ENCODER_COUNTS_PER_REVOLUTION = 20
  WHEEL_RADIUS = 5
  WHEEL_CIRCUMFERENCE = math.pi * WHEEL_RADIUS ** 2
  WHEEL_INCHES_PER_COUNT = WHEEL_CIRCUMFERENCE / ENCODER_COUNTS_PER_REVOLUTION
  
  def __init__(self):
      self.left_encoder_counts = 0
      self.right_encoder_counts = 0
      self.coordinates = (0, 0)
      self.angle = 0
      self.explore = True
      self.communicator = Communicator()
      self.wall_map = WallMap()
      self.ui = BotDisplay()
      self.state = "normal_stop"
      
  def main(self):
    while(self.explore):
      new_data = self.communicator.get_data()
      if new_data is None:
        time.sleep(.1)#delay for .1 seconds to let the program catch up
        continue
      self.wall_map.update_map(self.coordinates, new_data)
      instruction = self.calculate_instruction(new_data)
      if instruction == "e_stop":
        self.communicator.stop_all()
        self.ui.display_state("e_stop")
      else:
        self.communicator.set_state(instruction)
        self.ui.set_state(instruction)
  

  def calculate_instruction(self):
    pass
    """
    todo: figure out a way to calculate the state based 
    """

    #todo: figure out the next step based on the current location and new data


#Apply transfromation to robot location
#Plot 2 point 
#Add arraylist of every data packet recieved

#called everytime a new data packet arrives
def update_robot_location(self, deltaAngle, deltaRencoder, deltaLeftencoder):
  #do math and update robot location to best estimate
  
#called everytime a new data pscket arrives
def add_point

#after a certain ammount of time--
#def calculateWallSegmentBased on Points

#def delete extraniious points -- calculate 
