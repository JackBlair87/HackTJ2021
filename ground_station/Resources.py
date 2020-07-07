import math
from math import pi
import os
from os import path
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class InfoPacket:

  def __init__(self, time = 0, state = 0, f_distance = 0, r_distance = 0, l_encoderCounts = 0, r_encoderCounts = 0, angle = 0, e_stopped = False):
    self.logger = Logger("InfoPacket")
    try:
      self.state = int(state)
      self.time = float(time)/1000
      self.right_distance = float(r_distance)
      self.front_distance = float(f_distance)
      self.left_encoder_counts = int(float(l_encoderCounts))
      self.right_encoder_counts = int(float(r_encoderCounts))
      self.rotation = float(angle)
      self.emergency_stopped = e_stopped
    except:
      self.logger.log("ERROR CREATING INFOPACKET")
    # if e_stopped.lower() == "false":
    #   self.emergency_stopped = False
    # elif e_stopped.lower() == "true":
    #   self.emergency_stopped = True    
    # else:
    #   print("Error converting e_stopped to boolean in class InfoPacket")
    
  def __str__(self):
    return "Time Stamp: " + str(self.time) + ", Current State: " + str(self.state) + ", Forward Distance: " + str(self.front_distance) + ", Right Distance: " + str(self.right_distance) + ", Total Left Encoder Movement: " + str(self.left_encoder_counts) + ", Total Right Encoder Movement: " + str(self.right_encoder_counts) + ", Rotation Angle: " + str(self.rotation) + ", Emergency Stopped: " + str(self.emergency_stopped) + "\n"


class WheelInfo():
        ENCODER_COUNTS_PER_REVOLUTION = 20
        WHEEL_RADIUS = 5 #in cm
        WHEEL_CIRCUMFERENCE = pi * WHEEL_RADIUS ** 2
        WHEEL_CM_PER_COUNT = WHEEL_CIRCUMFERENCE / ENCODER_COUNTS_PER_REVOLUTION

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

class Logger():

  #maybe use singleton here?
  created = False
  outfolder = None
  outfile = None
  out_data_packets = None
  start_time = int(round(time.time() * 1000))

  def __init__(self, fromClass, outfolder="logs/outfile4"):
    self.fromClass = fromClass
    if Logger.created is True: #if a Logger has already been made, return log that and return false
      self.log("Files have already been created, continuing")
      return None
      self.start_time = int(round(time.time() * 1000))
    Logger.outfile = outfolder + "/all_logs.txt"
    Logger.out_data_packets = outfolder + "/info_packets.txt"
    if not os.path.exists(outfolder):#make the folder if necessary
      os.makedirs(outfolder)
    with open(Logger.outfile, "w+") as f:
      f.write("Beginning output for all logs:\n")
    with open(Logger.out_data_packets, "w+") as f:
      f.write("Beginning output for data packets:\n")
    self.log("Creating logger object")
    Logger.created = True

  def log(self, *text, end='\n', printToScreen=True, sep=" "):
    printString = str(self.get_time()) + ":" + self.fromClass + ": "
    for t in text:
      printString += str(text) + sep
    printString += end
    if printToScreen:
      print(printString, end='')
    with open(Logger.outfile, 'a') as f:
      f.write(printString)
  
  def logDataPacket(self, *text, end = '\n', printToScreen=True, sep=" "):
    printString = str(self.get_time()) + ":" + self.fromClass + ": "
    for t in text:
      printString += str(text) + sep
    printString += end
    if printToScreen:
      print(printString, end='')
    with open(Logger.outfile, 'a') as f:#writes to the main file
      f.write(printString)
    with open(Logger.out_data_packets, 'a') as f:#writes to data packet file
      f.write(printString)

  def get_time(self):
    return int(round(time.time() * 1000)) - self.start_time
  
class Colors:
  BLACK = (30, 30, 30)
  DBLACK = (10, 10, 10)
  WHITE = (167, 167, 167)
  GREEN = (75, 192, 168)
  DBLUE = (0, 116, 194)
  TAN = (184, 130, 109)
  BLUE = (85, 154, 212)
  PINK = (197, 134, 192)

class RegressionCalculator():
  def __init__(self, regression=None, x_train=None, y_train=None):
    if x_train is not None and y_train is not None:
      self.calculate_regression(x_train, y_train)
    else:
      self.regression = regression
      self.slope = None
      self.b = None
  
  def calculate_regression(self, x_train, y_train):
    x_train = [[elem] for elem in x_train]
    y_train = [[elem] for elem in y_train]

    self.regression = LinearRegression()
    self.regression.fit(x_train, y_train)
    self.slope = self.regression.coef_[0][0]
    self.b = self.regression.intercept_[0]
  
  def calculate_distance(x, y):
    if self.slope == 0:
        return y - (self.slope * x + self.b)
    perp_slope = -1 / self.slope
    perp_b = (y - perp_slope * x)
    intersect_x = (b - perp_b) / (perp_slope - self.slope)
    intersect_y = intersect_x * self.slope + self.b
    distance = math.sqrt((intersect_y-y)**2 + (intersect_x-x)**2)
    return distance

  def y_prediction(x):
    regressor.predict(x)