// -----
// RobotServos.h - Library for using servos advancedly.
// This class is implemented for use with the Arduino environment.
// Created by Jack Blair
// -----

#ifndef DistanceEstimator_h
#define DistanceEstimator_h

#include "Arduino.h"
#include "Ultrasonic.h"

class DistanceEstimator
{
public:

  // ----- Constructor -----
  DistanceEstimator(int e, int t);
  
  double getAverage();

  double calculateAverage();

  void record();

  void printList();

  boolean containsZero();

private:
  int echoPin, trigPin; // Arduino pins used for the servos. 

  int currentIndex;

  double average;

  int nullDistanceValue;

  double distances[3];
};

#endif