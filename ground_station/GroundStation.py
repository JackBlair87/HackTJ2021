import time

class Mode(): 
  stop = 0
  explore = 1
  sweep = 2
  manual = 3
  emergency_stop = 4
  #a list for easier debugging
  all_modes = ['stop', 'explore', 'sweep', 'manual', 'emergency_stop']
    
class State():
  stop = 0
  forward = 1
  reverse = 2
  turn_left = 3
  turn_right = 4
  error = -1
  all_states = ['stop', 'forward', 'reverse', 'turn_left', 'turn_right', 'error']
  
class GroundStation:
  def __init__(self):
      #self.wall_map = WallMap()
      self.ui = BotDisplay()
      self.mode = Mode.stop
      
  def main(self):
    #to be deleted method
    while(True):
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
      
  def manual_drive(self):
    if new_state != self.state: #if the state is the same as before, no change is necessary
      self.robot.set_state(new_state)
    
  def calculate_instruction(self):
    pass
    """
    todo: figure out a way to calculate the state based 
    """
    #robot.

    #todo: figure out the next step based on the current location and new data
  


#Apply transfromation to robot location
#Plot 2 point 

#called everytime a new data packet arrives

# def add_point

#after a certain ammount of time--
#def calculateWallSegmentBased on Points

#def delete extraniious points -- calculate 