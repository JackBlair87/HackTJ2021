#include <TimedAction.h> //MultiThreading Library
#include <RobotServos.h> //Servo Library
#include <MPU9250.h> //Gyro Library
#include <DistanceEstimator.h> //Distance Sensor Library
#include <RotaryEncoder.h> //Rotary Encoder Library
#include <SoftwareSerial.h> //Bluetooth Library

#define ledPin 13
#define BUFFER_SIZE 64 //This will prevent buffer overruns.
char inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
char inChar=-1;//Initialie the first character as nothing
int i=0;//Arduinos are not the most capable chips in the world so I just create the looping variable once

RobotServos servos(6, 5);
DistanceEstimator dF(8, 7);
DistanceEstimator dR(10, 9);
//MPU9250 mpu;
SoftwareSerial serial_connection(11, 12); //Create a serial connection with TX and RX on these pins
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
//-----------------------------------------------

void setup(){
  pinMode(ledPin, OUTPUT);
  Serial.begin(baudRate); //Initialize communications to the serial monitor in the Arduino IDE
  serial_connection.begin(baudRate); //Initialize communications with the bluetooth module
  //Wire.begin();
  //delay(2000);
  //mpu.setup();
}

void recieveData(){
  byte byte_count = serial_connection.available();//This gets the number of bytes that were sent by the python script
  if(byte_count) //If there are any bytes then deal with them
  {
    int first_bytes=byte_count;//initialize the number of bytes that we might handle. 
    int remaining_bytes=0;//Initialize the bytes that we may have to burn off to prevent a buffer overrun
    if(first_bytes>=BUFFER_SIZE-1)//If the incoming byte count is more than our buffer...
    {
      remaining_bytes=byte_count-(BUFFER_SIZE-1);//Reduce the bytes that we plan on handleing to below the buffer size
    }
    for(i=0;i<first_bytes;i++)//Handle the number of incoming bytes
    {
      inChar=serial_connection.read();//Read one byte
      inData[i]=inChar;//Put it into a character string(array)
    }
    inData[i]='\0';//This ends the character array with a null character. This signals the end of a string
    
    for(i=0;i<remaining_bytes;i++)//This burns off any remaining bytes that the buffer can't handle.
    {
      inChar=serial_connection.read();
    }

    Serial.print("Recieved New State: ");
    Serial.println(inData[0] - '0');//Print to the monitor what was detected
    state = inData[0] - '0';
    servos.setState(state);
  }
}

void transmitData(){
  if(Serial.availableForWrite()){
    serial_connection.println(String(millis()) + "," + String(state) + "," + String(dR.getAverage()) + "," + String(dR.getAverage()) + "," + String(-totalTravelL) + "," + String(totalTravelR) + "," + String(120.020));
  }
  //Example --> 12330,0,12.0,34.0,-48,-39,20.342
  //Serial.println(String(millis()) + "," + String(state) + "," + String(" ") + "," + String(" ") + "," + String(totalTravelL) + "," + String(totalTravelR) + "," + String(120.20));
  //Serial.println(String(mpu.getYaw()));
}

void encoderCheck(){
  rightEncoder.tick();
  leftEncoder.tick();
  totalTravelR = rightEncoder.getPosition();
  totalTravelL = leftEncoder.getPosition();

  int differenceR = rightEncoder.getPosition() - totalTravelR; //Larger int is positive change
  int differenceL = leftEncoder.getPosition() - totalTravelL;
 
//switch one of these to less than because of opposite spinning direction
  if((differenceL > servoTolerance || differenceR > servoTolerance) && state == 0){
    state = 0; //stops
    Serial.println("Error: Too much encoder movement while in 'Stopped' State --> increase servo tolerance");
  }

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
}


TimedAction recieve = TimedAction(50, recieveData);
TimedAction transmit = TimedAction(500, transmitData);

void loop(){
  refreshVariables();
  recieve.check();
  transmit.check();
}
