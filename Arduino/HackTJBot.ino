//Arduino
#include <TimedAction.h> //MultiThreading Library
#include <RobotServos.h> //Servo Library
#include <MPU9250.h> //Gyro Library
#include <DistanceEstimator.h> //Distance Sensor Library
#include <RotaryEncoder.h> //Rotary Encoder Library
#include <SoftwareSerial.h> //Bluetooth Library

#define ledPin 13
RobotServos servos(8, 7);
//DistanceEstimator dF(12, 11);
DistanceEstimator dR(10, 9);
RotaryEncoder rightEncoder(A2, A3);
RotaryEncoder leftEncoder(A0, A1);
//set up gyro A4 A5
SoftwareSerial serial_connection(10, 11); //Create a serial connection with TX and RX on these pins

//Global Variables ------------------------------
int state = 1;
      //0, Stop; 1, Forward; 2, Reverse; 3, Turn Left; 4, Turn Right; Other, LED on 
int totalTravelR = 0;
int totalTravelL = 0;
int changeTravelR = 0; //Difference since last transmission
int changeTravelL = 0;

int stopValRight = 0;
int stopValLeft = 0;
int servoTolerance = 2; //number of encoder step shifts when stopped

double stoppingBenchmark = 2; //cm
//-----------------------------------------------

void setup(){
  pinMode(ledPin, OUTPUT);
  Serial.begin(57600);
}

void checkComms(){
  //send
 Serial.print("Data Packet: ");
    Serial.print("(State)");
    Serial.print(state);
    Serial.print(", ");
    Serial.print("(Change L)");
    Serial.print(changeTravelL);
    Serial.print(", ");
    Serial.print("(Change R)");
    Serial.print(totalTravelR);
    Serial.print(", ");
    //Serial.print("(Distance F)");
    //Serial.print(dF.getAverage());
    //Serial.print(", ");
    Serial.print("(Distance R)");
    Serial.print(dR.getAverage());
    Serial.println(", ");

//recieve
  //set state to new state
  //set servo state to new state

    
    //Serial.print(totalTravelL);
    //Serial.print(", ");
    //Serial.println(totalTravelR);
    
    changeTravelR = 0;
    changeTravelL = 0;

    //Give back State
    //Give back encoder distances --> total moved and change
    //Give back distance readings
    //Give back angle readings
    
}

void encoderCheck(){
  rightEncoder.tick();
  leftEncoder.tick();

  int differenceR = rightEncoder.getPosition() - totalTravelR; //Larger int is positive change
  int differenceL = leftEncoder.getPosition() - totalTravelL;
  totalTravelR = rightEncoder.getPosition();
  totalTravelL = leftEncoder.getPosition();
  changeTravelR += differenceR;
  changeTravelL += differenceL;

//switch one of these to less than because of opposite spinning direction
  if((differenceL > servoTolerance || differenceR > servoTolerance) && state == 0){
    state = 0; //stops
    Serial.println("Error: Too much encoder movement while in 'Stopped' State --> increase servo tolerance");
  }

  //check state and encoder direction
  
}

void refreshVariables(){
  encoderCheck();
  dR.record();
  
  //dF.record();

  //if(dF.getAverage() <= stoppingBenchmark || dR.getAverage() <= stoppingBenchmark){      //may change
    //state = 0; //stops
  //}

 if(dR.getAverage() <= stoppingBenchmark && dR.getAverage() != -1){      //may change
    state = 0; //stops
  }
  else{
    state = 1;
  }
  
  servos.setState(state);
}

TimedAction commsCheck = TimedAction(500, checkComms);
//------------------------------------------------------------------------Actual Code----------------------------------------------------------------
void loop(){
  refreshVariables();
  commsCheck.check();
}
