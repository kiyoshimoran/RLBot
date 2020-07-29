from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from util.vec import Vec3
#from rlutilities.mechanics import WaveDash
from Actions.Action import Action
from Decisions.info import MyInfo
from util.sequence import Sequence, ControlStep
import math

class kickoff(Sequence):
    def __init__(self, loc):
        self.side = get_side(loc)
        self.name = "kickoff"
        # drive, diagonal flip, drive, front flip
        if is_diagonal(loc):
            print("Diagonal kickoff")
            steps = [
            ControlStep(duration=0.45, controls=SimpleControllerState(throttle=1, boost=True, steer=.25*self.side)),
            ControlStep(duration=0.1, controls=SimpleControllerState(throttle=1, boost=True, jump=True)),
            ControlStep(duration=0.1, controls=SimpleControllerState(throttle=1, jump=False, yaw=-self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(throttle=1, jump=True, yaw=-self.side, pitch=-1)),
            ControlStep(duration=0.15, controls=SimpleControllerState(throttle=1, boost=True, yaw=0.75*self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(boost=True, yaw=-0.75*self.side, pitch=-1)),
            ControlStep(duration=0.05, controls=SimpleControllerState(boost=True, steer=0.5*self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, boost=True, steer=0, yaw=0)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.1, controls=SimpleControllerState(jump=True, pitch=-1, yaw=0, steer=0)),
            ControlStep(duration=0.2, controls=SimpleControllerState())
            ]
        elif self.side != 0:
            print("Long kickoff")
            steps = [
            ControlStep(duration=0.6, controls=SimpleControllerState(throttle=1, boost=True, steer=-0.2*self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(throttle=1, jump=True)),
            ControlStep(duration=0.15, controls=SimpleControllerState(throttle=1, jump=False)),
            ControlStep(duration=0.05, controls=SimpleControllerState(throttle=1, jump=True, yaw=0.7*self.side, pitch=-1)),
            ControlStep(duration=0.1, controls=SimpleControllerState(throttle=1, pitch=-1, yaw=.2*self.side)),
            ControlStep(duration=0.1, controls=SimpleControllerState(throttle=1, yaw=0, steer=.2*self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.1, controls=SimpleControllerState())
            ]
        else:
            print("Straight kickoff")
            steps = [
            ControlStep(duration=0.7, controls=SimpleControllerState(throttle=1, boost=True, steer=-0.1*self.side)),
            ControlStep(duration=0.05, controls=SimpleControllerState(throttle=1, jump=True)),
            ControlStep(duration=0.15, controls=SimpleControllerState(throttle=1, jump=False)),
            ControlStep(duration=0.05, controls=SimpleControllerState(throttle=1, jump=True, yaw=0.7*self.side, pitch=-1)),
            ControlStep(duration=0.1, controls=SimpleControllerState(throttle=1, pitch=-1, yaw=.2*self.side)),
            ControlStep(duration=0.2, controls=SimpleControllerState(throttle=1, yaw=0, steer=.2*self.side, boost=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.1, controls=SimpleControllerState())
            ]
        super().__init__(steps)
        '''dash = WaveDash(self.car)
        while not dash.finished:
            dash.step()'''

def is_diagonal(loc):
    return abs(loc.y) < 2900

def get_side(loc):
    if loc.x == 0:
        return 0
    return -loc.x / abs(loc.x)
