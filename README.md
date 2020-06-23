# HackTJ2021
This is a project to develop an autonomous robot that maps its surroundings. The robot hardware consists of two ultrasonic sensors mounted on a frame with two continuous rotation servos. Separate encoders are attached to the robot. The encoders are not directly attached to the wheels, so they can provide independent data. 

The project consists of two parts: the robot and the groundstation. The robot colelcts raw data using its sensors (two ultrasonic distance sensors, two encoders, and a gyroscope) and sends the information to the groundstation via bluetooth. The groundstation (a laptop) will process the information and calculate the location of the robot at any given moment, as well as a map of the room.

As the robot learns more about the room, the goal is to use previous information to reinforce future information. For example, if we know that the robot is in a corner, we can combine the distance sensor data and the encoder data to update the map with more accurate information.

The robot will be programmed in Arduino, and the groundstation will be programmed in Python. We are using Python since we anticipate that it will have the most libraries related to Arduino, and for rapid development and ease of use.

 - The Team: Jack Blair, Akash Pamal, and Rahel Selemon

Arduino is a folder that contains the code that will be run on the Arduino. This project is in python, not the Arduino programming language, so the arduino files cannot be compiled or error-checked on this platform. Because of this, we develop the code separately on the Arduino IDE or online IDE, and copy and paste the code into text files in the arduino folder.
