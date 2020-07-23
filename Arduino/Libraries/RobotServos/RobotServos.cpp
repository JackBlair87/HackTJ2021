// -----
// RobotServos.h - Library for using servos advancedly.
// This class is implemented for use with the Arduino environment.
// Created by Jack Blair
// -----

#include "Arduino.h"
#include "RobotServos.h"
#include "Servo.h"

// ----- Initialization and Default Values -----

RobotServos::RobotServos(int rightPin, int leftPin) {
  
  // Remember Hardware Setup
  rightServoPin = rightPin;
  leftServoPin = leftPin;
  
  currentState = State::STOP;
  currentIntState = 0;
} 

int RobotServos::getState() {
  return currentIntState;
}

void RobotServos::setState(int newPosition) {
  if(newPosition > 4 || newPosition < 0){
    Serial.println("Servo Error: Invalid Number");
    rServo.detach();
    lServo.detach();
  }

  if(newPosition != currentIntState){
    currentIntState = newPosition;
    switch (newPosition) {
      case 0:
      currentState = State::STOP;
        rServo.detach();
        lServo.detach();
        Serial.println("Vehicle Stopped");
        break;
      case 1:
        currentState = State::FORWARD;
        rServo.attach(rightServoPin);
        lServo.attach(leftServoPin);
        lServo.write(maxBackward);
        rServo.write(maxForward);
        Serial.println("Vehicle Forward");
        break;
      case 2:
        currentState = State::REVERSE;
        rServo.attach(rightServoPin);
        lServo.attach(leftServoPin);
        lServo.write(maxForward);
        rServo.write(maxBackward);
        Serial.println("Vehicle Backward");
        break;
      case 3:
        currentState = State::LEFT;
        rServo.attach(rightServoPin);
        lServo.attach(leftServoPin);
        lServo.write(maxForward);
        rServo.write(maxForward);
        Serial.println("Vehicle Turning Left");
        break;
      case 4:
        currentState = State::RIGHT;
        rServo.attach(rightServoPin);
        lServo.attach(leftServoPin);
        lServo.write(maxBackward);
        rServo.write(maxBackward);
        Serial.println("Vehicle Turning Right");
        break;
      }
  }
}

  void RobotServos::inverse() {
    int x = maxBackward;
    maxBackward = maxForward;
    maxForward = x;
    Serial.println("Servo direction inversed");
  }