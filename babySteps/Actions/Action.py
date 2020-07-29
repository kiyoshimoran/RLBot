from rlbot.agents.base_agent import GameTickPacket, SimpleControllerState
from Drawing.Drawing import DrawingTool
from Decisions.info import MyInfo, Car
from math import pi

class Action:
    
    def __init__(self):
        #self.car = car
        self.controls : SimpleControllerState = SimpleControllerState()
        #self.controls: Input = Input()
        self.last_touch = None
        self.done: bool = False
        self.drift_angle = 0.785398 #45 degrees in radians
        self.drift_dist = 2000
        self.name = None


    def steeringMagic(self, angle):
        '''
        if angle > pi: 
            print("angle over 180")
            angle = (2 * pi) - angle
        elif angle < -pi:
            print("angle under 180")
            angle = (-2 * pi) - angle

        if angle > self.drift_angle:
            angle = self.drift_angle - (angle * self.drift_angle / pi)
        elif angle < -self.drift_angle:
            angle = -self.drift_angle + (angle * self.drift_angle / pi)
    '''
        if angle > 1:
            return 1
        if angle < -1:
            return -1
        return angle

    def new_touch(self, info : MyInfo):
        if self.last_touch != info.last_touch.time_seconds:
            self.done = True
            print("new touch")
            return True
        return False


    def tick(self, info : MyInfo) -> SimpleControllerState:
        pass

    def interruptible(self) -> bool:
        return True

    def render(self, draw: DrawingTool):
        pass