#to work, this class must be moved out of the "tests" folder and into the "ground_station" folder

from Resources import Logger


logger1 = Logger(fromClass="Class1")
logger2 = Logger(fromClass="Class2")


logger1.log("Hello")
logger2.log("Goodbye")