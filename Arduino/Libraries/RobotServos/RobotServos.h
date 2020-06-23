// -----
// RobotServos.h - Library for using servos advancedly.
// This class is implemented for use with the Arduino environment.
// Created by Jack Blair
// -----

#ifndef RobotServos_h
#define RobotServos_h

#include "Arduino.h"
#include "Servo.h"

class RobotServos
{
public:
  enum class State { STOP = 0, FORWARD = 1, REVERSE = 2, LEFT = 3, RIGHT = 4, ERROR = -1};

  // ----- Constructor -----
  RobotServos(int rightPin, int leftPin);
  
  // simple retrieve of the state
  int getState();

  // adjust the current state
  void setState(int newPosition);

  void inverse();

private:
  int rightServoPin, leftServoPin; // Arduino pins used for the servos. 

  int maxForward = 180, maxBackward = 0;

  int stopValRight, stopValLeft; //Should be around 90

  State currentState;
  int currentIntState;

  Servo rServo, lServo;
};

#endif

// End