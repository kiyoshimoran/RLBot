from Actions.Action import Action
from Actions.Challenge import challenge
from Drawing.Drawing import DrawingTool
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.sequence import StepResult
from util.orientation import Orientation, relative_location
from util.vec import Vec3
from Decisions.info import MyInfo, Car
from Decisions.challengeGame import ChallengeGame


from math import pi 
from math import atan2

CHALLENGE_TIME = 0.3
ZERO_SPEED = 0.3

class shadow(Action):

    def __init__(self, info) -> SimpleControllerState:
        super().__init__()
        self.info = info
        self.last_touch = info.last_touch.time_seconds
        self.car = info.car
        self.cg = ChallengeGame(self.info.car, self.info)
        self.o_cg = ChallengeGame(self.info.opp_car, self.info)
        self.name = "Shadow"

    def tick(self, info : MyInfo):
        self.new_touch(info)
        if self.can_challenge():
            self.done = True
        #print("last touch: {}".format(self.last_touch))
        ball = self.info.ball_path[0].physics
        target = Vec3(self.info.my_goal.center) - ball.location
        relative = relative_location(Vec3(self.car.loc), Orientation(self.car.rot), Vec3(ball.location))
        angle = atan2(relative.y, relative.x)
        self.controls.steer = self.steeringMagic(angle)
        boost, throttle = self.match_speed(self.car, ball)
        self.controls.boost = boost
        self.controls.throttle = throttle
        return self.controls

    def can_challenge(self):
        ball_loc = Vec3(self.info.ball_path[0].physics.location)
        my_ttb = self.cg.get_time_to_loc(ball_loc)
        op_ttb = self.o_cg.get_time_to_loc(ball_loc)
        if op_ttb - CHALLENGE_TIME > my_ttb:
            return True
        return False


    def match_speed(self, car : Car, ball):
        boost = False
        throttle = 1
        my_speed = car.vel.flat().length()
        ball_speed = Vec3(ball.velocity).flat().length()
        if ball_speed > my_speed:
            boost = True
        elif my_speed == 0:
            throttle = ZERO_SPEED
        else:
            throttle = ball_speed / my_speed
        return boost, throttle
