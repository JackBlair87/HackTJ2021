// -----
// DistanceEstimator.h - Library for estimating distances correctly.
// This class is implemented for use with the Arduino environment.
// Created by Jack Blair
// -----

#include "Arduino.h"
#include "DistanceEstimator.h"
#include "Ultrasonic.h"

// ----- Initialization and Default Values -----

DistanceEstimator::DistanceEstimator(int e, int t) {
  
  // Remember Hardware Setup
  echoPin = e;
  trigPin = t;
  
  average = 0;
  nullDistanceValue = 250;
} 

double DistanceEstimator::getAverage() {
  if(average == -1){
    Serial.println("Error: Not enough distance data to fill array");
  }
  return average;
}

void DistanceEstimator::record(){
  Ultrasonic u(echoPin, trigPin, 40000UL);
  double reading = u.read(INC);
  
  if(reading < nullDistanceValue && reading >= 0){ //check if reading is valid
    distances[currentIndex % 3] = reading;
    currentIndex++;
    if(!containsZero()){
      average = calculateAverage();
    }
    else{
      average = -1;
    }
  }
  else{
    distances[currentIndex % 3] = 0;
    currentIndex++;
    average = -1;
  }
}

void DistanceEstimator::printList(){
  Serial.print("[");
  Serial.print(distances[0]);
  Serial.print(", ");
  Serial.print(distances[1]);
  Serial.print(", ");
  Serial.print(distances[2]);
  Serial.print("]");
  Serial.println("");
}

boolean DistanceEstimator::containsZero(){
  for(int x = 0; x < 3; x++){
    if(distances[x] == 0){
      return true;
    }
  }
  return false;
}

double DistanceEstimator::calculateAverage(){
  double sum = 0;
  for(int x = 0; x < 3; x++){
    sum += distances[x];
  }
  return sum/3;
}