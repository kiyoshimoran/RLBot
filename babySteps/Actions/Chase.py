from Actions.Action import Action
from Drawing.Drawing import DrawingTool
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.sequence import StepResult
from util.orientation import Orientation, relative_location
from util.vec import Vec3
from Decisions.info import MyInfo, Car

from math import pi 
from math import atan2

OFFSET_LEN = 50

class chase(Action):
    def __init__(self, car : Car, info, target_dest : Vec3) -> SimpleControllerState:
        super().__init__()
        self.info = info
        self.car = car
        self.name = "Chase"
        #self.dest = Vec3(target_dest.x, target_dest.y, target_dest.z)
        #self.dest = self.info.ball.position
        
        '''
        self.drive = Drive(car)
        self.drive.target = Vec3(dest.x, dest.y, dest.z)
        self.action = self.drive
        

        car_to_ball_vec = (self.dest - self.car.position)
        self.dist_to_ball = car_to_ball_vec.length()
        #car_to_ball_angle = angle_between(xy(self.car.position), xy(car_to_ball_vec))

        rel_angle = atan2(car_to_ball_vec[1], car_to_ball_vec[0])
        print(self.car.rotator)
        rot = atan2(self.car.velocity[1], self.car.velocity[0])
        self.angle_to_ball = rel_angle - rot
        if self.angle_to_ball > self.drift_angle and self.dist_to_ball < self.drift_dist:
            self.controls.handbrake = 1
        else:
            self.controls.handbrake = 0

        #steering_angle = car_to_ball_angle / self.steering_scale
        steering_angle = self.steeringMagic(self.angle_to_ball)
        print("steering angle is: {}, drift = {}".format(steering_angle, self.controls.handbrake))
        if abs(steering_angle) > 0.01:
            self.controls.steer = steering_angle
        else: 
            self.controls.steer = 0
        self.controls.throttle = 1
        '''

    def tick(self, info : MyInfo) -> SimpleControllerState:
        self.new_touch(info)
        target = Vec3(self.info.ball_path[0].physics.location)
        offset = (Vec3(target) - self.info.their_goal.center).rescale(OFFSET_LEN)
        #print("in tick: target = {}".format(target))

        relative = relative_location(Vec3(self.car.loc), Orientation(self.car.rot), target + offset)
        angle = atan2(relative.y, relative.x)
        other_ang = self.car.vel.ang_to(target)
        #print("relative: {}".format(relative))
        #print("angle to ball: {}, other angle: {}".format(angle * 180 / pi, other_ang * 180 / pi))
        self.controls.steer = self.steeringMagic(angle * 5)
        self.controls.throttle = 1
        return self.controls

    def render(self, draw: DrawingTool):
        str_car = "xy vec = {}, norm = {}".format(xy(self.car.velocity), norm(xy(self.car.velocity)))
        str_car_pos = "car at {}".format(xy(self.car.position))
        str_dest = "destination: {}".format(self.dest)
        str_angle = "angle to dest = {}".format(self.angle_to_ball * 180 / pi)
        str_steer = "steering angle = {}".format(self.controls.steer)
        draw.draw_circle(self.dest)
        draw.artist.begin_rendering("chase")
        draw.artist.draw_string_2d(50, 260, 1, 1, str_car, draw.artist.black())
        draw.artist.draw_string_2d(50, 280, 1, 1, str_angle, draw.artist.black())
        draw.artist.draw_string_2d(50, 300, 1, 1, str_dest, draw.artist.black())
        draw.artist.draw_string_2d(50, 320, 1, 1, str_steer, draw.artist.black())
        draw.artist.draw_string_2d(50, 340, 1, 1, str(self.dist_to_ball), draw.artist.black())
        draw.artist.draw_string_2d(50, 360, 1, 1, str_car_pos, draw.artist.black())
        draw.artist.end_rendering()
