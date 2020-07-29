from util.vec import Vec3
from Drawing.Drawing import DrawingTool
from Decisions.info import MyInfo
from rlbot.utils.structures.ball_prediction_struct import Slice, BallPrediction


class ChallengeGame:
    challenge_loc : Vec3
    challenge_vec : Vec3
    best_ttb : float
    time : float
    winnable : bool
    fifty : bool
    should_go : bool


    def __init__(self, car, info : MyInfo):
        self.car = car
        self.info = info
        #self.calc_best_ttb(car, ball_path)
        self.should_go = True
        self.challenge_loc = Vec3(info.ball_path[0].physics.location)

    def get_time_to_loc(self, loc : Vec3):
        scale = 1
        dist_to_target = loc.dist(self.car.loc)
        speed = self.car.vel.length()
        temp = (dist_to_target / 2) ** 2
        #approximate curvature
        magicNum = (speed ** 2) / ((self.car.vel.length() ** 2) + temp)
        
        time = dist_to_target * scale / speed / magicNum
        #print("curve: {}, d / s: {}".format(magicNum, dist_to_target / speed ))
        return time

'''
    def get_time_to_loc(self, my_loc, vec, dest):
        magic_turning_number = 4
        #loc = Vec3(dest.x, dest.y, dest.z)
        my_loc = Vec3(my_loc[0], my_loc[1], my_loc[2])
        car_to_ball_vec = my_loc - dest
        dist_to_ball = car_to_ball_vec.length()
        car_to_ball_angle = vec.ang_to(car_to_ball_vec)
        turn_time = car_to_ball_angle * magic_turning_number
        self.turn = turn_time
        if norm(vec) == 0:
            vec = Vec3(700, 700, 0)
        straight_time = dist_to_ball / norm(xy(vec))
        self.straight = straight_time
        return turn_time + straight_time


    #get fastest intercept time
    def calc_best_ttb(self, car, ball_pred_slices):
        ball_path = ball_pred_slices.physics.location
        vel = car.vel
        pos = car.loc
        dest = ball_path[-1]
        
        ttb = self.get_time_to_loc(pos, vel, dest)
        for i in range(len(ball_path)):
            temp = self.get_time_to_loc(pos, vel, ball_path[i])
            if temp < ttb:
                ttb = temp
                dest = ball_path[i]
        self.challenge_loc = dest
        self.best_ttb = ttb

    def render(self, draw: DrawingTool):
        text = "ttb = {}".format(self.ttb)
        turn = "turn = {}".format(self.turn)
        straight = "straight = {}".format(self.straight)
        draw.artist.begin_rendering("ttb")
        draw.artist.draw_string_2d(50, 200, 1, 1, text, draw.artist.black())
        draw.artist.draw_string_2d(50, 220, 1, 1, turn, draw.artist.black())
        draw.artist.draw_string_2d(50, 240, 1, 1, straight, draw.artist.black())
        draw.artist.end_rendering()
'''