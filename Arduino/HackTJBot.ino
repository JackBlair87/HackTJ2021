#include <MPU9250.h> //Gyro Library
#include <RGBLamp.h> //RGB LED Library
#include <TimedAction.h> //MultiThreading Library
#include <RobotServos.h> //Servo Library
#include <RotaryEncoder.h> //Rotary Encoder Library
#include <SoftwareSerial.h> //Bluetooth Library
#include <NewPing.h> //Ultrasonic Distance Sensor Library

RGBLamp led;
RobotServos servos(7, 6);
NewPing sonarF(9, 8, 200); // NewPing setup of pins and maximum distance.
NewPing sonarR(10, 11, 200); // NewPing setup of pins and maximum distance.
SoftwareSerial groundStation(12, 13); //Create a serial connection with TX and RX on these pins
MPU9250 mpu;
RotaryEncoder rightEncoder(A2, A3);
RotaryEncoder leftEncoder(A0, A1);

int state = 0; //0, Stop; 1, Forward; 2, Reverse; 3, Turn Left; 4, Turn Right; Other, LED on 
boolean isConnected = false;
int nullCount = 0;
int baudRate = 9600;
int distances[2] = {0, 0};
int totalTravelR = 0;
int totalTravelL = 0;
int servoTolerance = 2; //number of encoder step shifts when stopped
double stoppingBenchmark = 2; //cm
byte someColors[6][3] = { {0, 0, 255}, {0, 255, 0}, {255, 0, 255}, {255, 147, 255}, {255, 255, 0}, {224, 5, 97} };

void setup(){
  Serial.begin(baudRate); //Initialize communications to the serial monitor in the Arduino IDE
  groundStation.begin(baudRate); //Initialize communications with the bluetooth module
 
  Wire.begin();
  delay(2000);
  mpu.setup();
  
  led.begin(COMMON_ANODE, 5, 4, 3);
  led.blink(Color::Red);
}

void(* resetFunc) (void) = 0; //declare reset function @ address 0

void recieveData(){
  if(groundStation.available()){
    int newState = state;
    nullCount = 0;
    while(groundStation.available() > 0){
      newState = groundStation.read() - '0';
    }
    if(newState > -1 && newState < 5){
      //Serial.println("Recieved New State: " + newState);
      state = newState;
      isConnected = true;
      led.setColor(someColors[state][0], someColors[state][1], someColors[state][2]);
    }
  }
  else{
    nullCount++;
    if(nullCount > 50 && isConnected){
      isConnected = false;
      state = 0;
      led.blink(Color::Red);
      Serial.println("Disconnected");
      //resetFunc();
    }
  }
}

void transmitData(){

recieveData();
  
  if(isConnected){
    groundStation.print(":" + String(state) + "," + String(distances[0]) + "," + String(distances[1]) + "," + String(totalTravelL) + "," + String(-totalTravelR) + "," + String(mpu.getYaw()) + ":");
    //groundStation.println(":2," + String(state) + "," + String(dR.getAverage()) + "," + String(dR.getAverage()) + "," + String(-totalTravelL) + "," + String(totalTravelR) + "," + String(mpu.getYaw()) + ":");
    //groundStation.println(":" + String(millis()) + "," + String(state) + "," + String(random(5, 10)) + "," + String(random(5, 10)) + "," + String(-totalTravelL) + "," + String(totalTravelR) + "," + String(random(0.00, 360.00)) + ":");
    //Serial.println(":" + String(state) + "," + String(dR.getAverage()) + "," + String(dR.getAverage()) + "," + String(-totalTravelL) + "," + String(totalTravelR) + "," + String(mpu.getYaw()) + ":");
    //Example --> :12330,0,12.07,34.04,-48,-39,20.342:
    //Serial.println("Transmitted Data");
  }
}

void refreshVariables(){
  rightEncoder.tick();
  leftEncoder.tick();
  totalTravelR = rightEncoder.getPosition();
  totalTravelL = leftEncoder.getPosition();
  mpu.update();
  
  if(servos.getState() != state){
    servos.setState(state);
  }
}

void sendPing(){
  distances[0] = sonarF.ping() / US_ROUNDTRIP_CM;
  distances[1] = sonarR.ping() / US_ROUNDTRIP_CM;
  //Serial.println(String(distances[0]) + ", " + String(distances[1]));
}

TimedAction transmit = TimedAction(10, transmitData);
TimedAction pinG = TimedAction(50, sendPing);
   
void loop(){
  refreshVariables();
  led.update(); //Run continuously
  transmit.check();
  pinG.check();
  Serial.println(millis());
}
