from Resources import Logger


logger1 = Logger(fromClass="Class1")
logger2 = Logger(fromClass="Class2")


logger1.log("Hello")
logger2.log("Goodbye")