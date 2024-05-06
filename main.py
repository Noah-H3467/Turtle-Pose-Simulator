import math
import threading
import time
#from TurtlePose import TurtlePose
from turtle import *

# timer.py - basic timer classes from RealPython

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

# Class to keep track of the current 2D position of a turtle, or a desired turtle position
class TurtlePose:

    # x, y, and rot are ints. rot represents degrees, turtle is a turtle object, and hideTurtle determines whether the turtle should be hidden.
    def __init__(self, x, y, rot, hideTurtle):
        self.x = x
        self.y = y
        self.rot = rot
        self.turtle = Turtle()
        if hideTurtle:
            self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.goto(x,y)
        self.turtle.setheading(rot)


    def setPos(self, x, y, rot):
        self.x = x
        self.y = y
        self.rot = rot
        self.turtle.goto(x, y)
        self.turtle.setheading(rot)

    def incrementRot(self, deltaRot):
        self.rot += deltaRot
        self.turtle.setheading(self.rot)

    def incrementXY(self, x, y):
        self.x += x
        self.y += y
        self.turtle.goto(x,y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getRot(self):
        return self.rot
    
    def printPos(self):
        print("Turtle Position | X: ", self.x, " Y: ", self.y, " Theta:", self.rot)

    def distanceFromOrigin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5


# Will likely get replaced by a Constants Class
class Constants:

    # PID for movement, PID for rotation, max velocity + acceleration for movement, max velocity + acceleration for rotation
    kP = 5
    kI = 5
    kD = 5
    kRotP = 5
    kRotI = 5
    kRotD = 5
    kMaxVelocity = 30
    kMaxAcceleration = 20
    kMaxAngularVelocity = 540
    kMaxAngularAcceleration = 600


class TrapezoidTurtlePID:



    # Inputs are two TurtlePose objects, one for the future (which you need to create), and one for the present (pass in Nocturne), and one TurtlePIDConstants object
    # Whatever you do, do NOT make the current and goal poses the same yet. That still needs to be worked out.
    def __init__(self, FuturePose, PresentPose, prevAngularVelocity):
        self.Pose2 = FuturePose
        self.Pose1 = PresentPose
        global deltaTime
        deltaTime = 0.04
            # Previous velocity should be from previous time running pid, default is 0
        previousVelocity = 0.0
        previousAngularVelocity = prevAngularVelocity
    #Takes the difference of the x, y, and theta attributes of the TurtlePose objects
        self.deltaX = self.Pose2.getX() - self.Pose1.getX()
        self.deltaY = self.Pose2.getY() - self.Pose1.getY()
        self.deltaTheta = self.Pose2.getRot() - self.Pose1.getRot()

        # Use Distance Formula
        DistanceToTarget = math.sqrt(self.deltaX ** 2 + self.deltaY ** 2)
        # Calculate Angle to target (this is NOT the rotation)
        # Whenever arctan is undefined
        DirectionToTarget = -367  #Out of range value to indicate an error
        if self.deltaX == 0 and self.deltaY > 0:
            DirectionToTarget = 90
            print("Wilky")
        elif self.deltaX == 0 and self.deltaY < 0:
            DirectionToTarget = -90
            print("Bryson")
        # Quadrants 1 and 4, arctan is fine
        elif self.deltaX > 0:
            #In radians, between +/- pi/2
            DirectionToTarget = math.atan(self.deltaY/self.deltaX)
            DirectionToTarget = DirectionToTarget*180/math.pi
            print("Chris")
        #Q2 and 180 degrees
        elif self.deltaX < 0 and self.deltaY >= 0:
            DirectionToTarget = math.atan(self.deltaY/self.deltaX)
            DirectionToTarget = DirectionToTarget*180/math.pi + 180
            print("Mr. K")
        #Q3
        elif self.deltaX < 0 and self.deltaY < 0:
            DirectionToTarget = math.atan(self.deltaY/self.deltaX)
            DirectionToTarget = DirectionToTarget*180/math.pi + 180
            print("Emille")
        # The Origin
        elif self.deltaX == 0 and self.deltaY == 0:
            print("You weren't supposed to have the same present and future position yet...to be worked on")
            DirectionToTarget = 0
        else:
            print("Uh Oh! Something went wrong")
        print(DirectionToTarget)

    # Then from maximum velocity we can calculate maximum distance
        m_velocity = deltaTime * Constants.kMaxAcceleration + previousVelocity
        if m_velocity > Constants.kMaxVelocity:
            m_velocity = Constants.kMaxVelocity
        # Multiply by time to get maximum Distance, because d = rt
        global m_distance
        m_distance = m_velocity * deltaTime
        print("MaxV: ", m_velocity)
        print("MaxDist: ", m_distance)
    
        # Calculate how much the heading of the turtle will change
        m_angularVelocity = deltaTime * Constants.kMaxAngularAcceleration + previousAngularVelocity
        if m_angularVelocity > Constants.kMaxAngularVelocity:
            m_angularVelocity = Constants.kMaxAngularVelocity
        # Multiply by time to get maximum Distance, because d = rt
        global m_rotate
        m_rotate = m_angularVelocity * deltaTime
        print("MaxAngleV: ", m_angularVelocity)
        print("MaxAngleRotation: ", m_rotate)

    #if the jump (distance and rotation) can hit the target, then go to the target
       # if MaxDistance == DistanceToTarget:
            #self.Pose2.setPos
        if m_distance > DistanceToTarget:
            # M_distance becomes the distance that we actually use
            m_distance = DistanceToTarget
        if m_rotate > self.deltaTheta:
            m_rotate = self.deltaTheta

        # Print the vector transformation
        print("Theta: ", m_rotate)
        print("r: ", m_distance)
        # Rotate As determined by trapezoid - no PID yet
        self.Pose1.incrementRot(m_rotate)
        # Next we use trig (theta and r) to find the new x and y components

        # Then increment x and y
        
    def printDeltaPose(self):
        print("Trapezoid PID Delta Pose | dX: ", self.deltaX, " dY: ", self.deltaY, " dTheta: ", self.deltaTheta)
    
    def getLinearVelocity(self):
        return m_distance / deltaTime

    def getAngularVelocity(self):
        return m_rotate / deltaTime




# Main class
#Not using periodic() right now due to main thread not in main loop error
def periodic(isFinished):
    x=0
    global Nocturne
    while isFinished.is_set():
        # 50 times per second, rotate Nocturne by 1 degree
        Nocturne.incrementRot(1)
        time.sleep(0.0187)   # Approx. 20 milliseconds between running is t = 0.0187
        x += 1



# Stuff from a python tutorial
#isFinished = threading.Event()
#isFinished.set()
#t = threading.Thread(target=periodic, args=(isFinished,))

# Create our robot turtle
space = Screen()
# global Nocturne
Nocturne = TurtlePose(0,0,0, False)

#Periodic loop

#t.start()
#starts timer from basic Timer class
clock = Timer()
clock.start()
# While time since starting clock Timer is less than x seconds - timer will stop after 10 seconds
###while time.perf_counter() - clock._start_time < 10:
    ## 25 times per second, rotate Nocturne by 1 degree
    #Nocturne.incrementRot(1)
    #time.sleep(0.001)   # Approx. 40 milliseconds between running is t = 0.0187


#isFinished.clear()
print("The timer has been stopped!")
Nocturne.printPos()
DesiredPose = TurtlePose(1, 0,180, True)

# How long does the PID take?
print("time", time.perf_counter() - clock._start_time)
NocturneTrapezoidPID = TrapezoidTurtlePID(DesiredPose, Nocturne, 0)
NocturneTrapezoidPID.printDeltaPose()
# Get angular Velocity to pass into the next time we create a PID, eventually do this with time (use time.perf_counter() in the trapezoidPID class) and linear velocity
angularVelocity = NocturneTrapezoidPID.getAngularVelocity()
print("time", time.perf_counter() - clock._start_time)

time.sleep(3)
print("time", time.perf_counter() - clock._start_time)
#Instead of doing a goofy ahh for loop figure out how to end the loop (use a boolean check in there) which should be a while loop.
for x in range(26):
    NocturneTrapezoidPID = TrapezoidTurtlePID(DesiredPose, Nocturne, angularVelocity)
    NocturneTrapezoidPID.printDeltaPose()
    angularVelocity = NocturneTrapezoidPID.getAngularVelocity()
print("time", time.perf_counter() - clock._start_time)

clock.stop()
time.sleep(5)

#the down part of the trapezoid will be PID controlled, but that is something for later