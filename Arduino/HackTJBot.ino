#include <TimedAction.h> //MultiThreading Library
#include <RobotServos.h> //Servo Library
#include <MPU9250.h> //Gyro Library
#include <DistanceEstimator.h> //Distance Sensor Library
#include <RotaryEncoder.h> //Rotary Encoder Library
#include <SoftwareSerial.h> //Bluetooth Library

#define ledPin 13
RobotServos servos(6, 5, 5);
DistanceEstimator dF(8, 7);
DistanceEstimator dR(10, 9);
//MPU9250 mpu;
SoftwareSerial groundStation(11, 12); //Create a serial connection with TX and RX on these pins
RotaryEncoder rightEncoder(A2, A3);
RotaryEncoder leftEncoder(A0, A1);

//Global Variables ------------------------------
int state = 0; //0, Stop; 1, Forward; 2, Reverse; 3, Turn Left; 4, Turn Right; Other, LED on 
int totalTravelR = 0;
int totalTravelL = 10;

int stopValRight = 0;
int stopValLeft = 0;
int servoTolerance = 2; //number of encoder step shifts when stopped

double stoppingBenchmark = 2; //cm
int baudRate = 9600;
int nullCount = 0;
boolean isConnected = false;
//-----------------------------------------------

void setup(){
  pinMode(ledPin, OUTPUT);
  Serial.begin(baudRate); //Initialize communications to the serial monitor in the Arduino IDE
  groundStation.begin(baudRate); //Initialize communications with the bluetooth module
  
  //Wire.begin();
  //delay(2000);
  //mpu.setup();
}

void recieveData(){
  if(groundStation.available()){
    int newState = state;
    nullCount = 0;
    while(groundStation.available() > 0){
      newState = groundStation.read() - '0';
    }
    if(newState > -1 && newState < 5){
      //Serial.println("Recieved New State");
      state = newState;
      isConnected = true;
    }
  }
  else{
    nullCount++;
  }

  if(nullCount > 1 && isConnected){
    isConnected = false;
    state = 0;
    Serial.println("Disconnected");
  }
}

void transmitData(){
  if(isConnected){
    groundStation.println(String(millis()) + "," + String(state) + "," + String(dR.getAverage()) + "," + String(dR.getAverage()) + "," + String(-totalTravelL) + "," + String(totalTravelR) + "," + String(random(0,270)));
    //Example --> 12330,0,12.0,34.0,-48,-39,20.342
    //Serial.println(String(millis()) + "," + String(state) + "," + String(" ") + "," + String(" ") + "," + String(totalTravelL) + "," + String(totalTravelR) + "," + String(120.20));
    Serial.println("Transmitted Data");
  }
}

void encoderCheck(){
  rightEncoder.tick();
  leftEncoder.tick();
  totalTravelR = rightEncoder.getPosition();
  totalTravelL = leftEncoder.getPosition();

  int differenceR = rightEncoder.getPosition() - totalTravelR; //Larger int is positive change
  int differenceL = leftEncoder.getPosition() - totalTravelL;
 
//switch one of these to less than because of opposite spinning direction
  //if((differenceL > servoTolerance || differenceR > servoTolerance) && state == 0){
    //state = 0; //stops
    //Serial.println("Error: Too much encoder movement while in 'Stopped' State --> increase servo tolerance");
  //}

  //check state and encoder direction
  
}

void refreshVariables(){
  encoderCheck();
  //dR.record();
  //mpu.update();
  
  //dF.record();

  //if(dF.getAverage() <= stoppingBenchmark || dR.getAverage() <= stoppingBenchmark){      //may change
    //state = 0; //stops
  //}

 //if(dR.getAverage() <= stoppingBenchmark && dR.getAverage() != -1){      //may change
    //state = 0; //stops
  //}
  //else{
    //state = 1;
  //}
  if(servos.getState() != state){
    servos.setState(state);
  }
}


TimedAction recieve = TimedAction(100, recieveData);
TimedAction transmit = TimedAction(500, transmitData);

void loop(){
  refreshVariables();
  recieve.check();
  transmit.check();
  Serial.println(state);
}
