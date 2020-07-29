from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import math
import time
from math import radians

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def r_velocity(car, ball):
    rxvel = ball.x - car.x
    ryvel = ball.y - car.y 
    v = math.sqrt(rxvel ** 2 + ryvel ** 2)
    if v == 0:
        v = 1
    return v

# Blue team's (0) goal is located at (0, -5120) 
# Orange (1) at (0, 5120)
# ball R = 92
class Bot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.controller = SimpleControllerState()
        #TODO read from cfg instead of hardcoding
        # Game values
        self.logger.info("\n\nMy car index is {}\n\n".format(self.index))
        self.bot_pos = None
        self.bot_vel = None
        self.bot_yaw = None
        self.bot_to_ball = 0
        # Contants
        self.scale = 1
        if self.team == 0:
            self.scale = -1
        self.TEAM_OFFSET = 75 
        if self.team == 0:
            self.TEAM_OFFSET = -75  
        self.DODGE_TIME = 0.2
        self.DODGE_HEIGHT = 300
        self.DISTANCE_TO_DODGE = 550
        self.DISTANCE_FROM_BALL_TO_BOOST = 1500 # The minimum distance the ball needs to be away from the bot for the bot to boost
        # The angle (from the front of the bot to the ball) at 1which the bot should start to powerslide.
        self.POWERSLIDE_ANGLE = 3

        # Dodging
        self.should_dodge = False
        self.on_second_jump = False
        self.next_dodge_time = 0

    def rotate(self, cars):
        '''
    	ball_prediction = self.get_ball_prediction_struct()
    	if ball_prediction is not None:
    		for i in range(0, ball_prediction.num_slices):
    			prediction_slice = ball_prediction.slices[i]
    			location = prediction_slice.physics.location
    			self.logger.info("At time {}, the ball will be at ({} {} {})".format(prediction_slice.game_seconds, location.x, location.y, location.z))
        '''
        vel = math.sqrt(self.bot_vel.x ** 2 + self.bot_vel.y ** 2)
        rvel = r_velocity(self.bot_vel, self.ball_vel)
        if vel == 0:
            vel = 1
        time_to_ball = self.bot_to_ball / rvel
        '''
        for car in cars:
            if car.team != self.team:
                d_other = distance(car.physics.location.x, car.physics.location.y, self.ball_pos.x, self.ball_pos.y)
                vel_other = math.sqrt(car.physics.velocity.x ** 2 + car.physics.velocity.y ** 2)
                rvel_other = r_velocity(car.physics.velocity, self.ball_vel)
                if vel_other == 0:
                    vel_other = 1
                other_time_to_ball = d_other / rvel_other
                 assumes teams
                if car.team == self.team:
                    if time_to_ball <= other_time_to_ball:
                    self.aim_car(self.ball_pos.x, self.ball_pos.y + self.TEAM_OFFSET)
                else:
                    self.cover_goal() 
                if time_to_ball <= other_time_to_ball:
                    self.logger.info("first to ball")
                    self.aim_car(self.ball_pos.x, self.ball_pos.y + self.TEAM_OFFSET)
                # Blue team's goal is located at (0, -5000) Orange at (0, 5000)
                else:
                    self.logger.info("beat to ball")
                    self.cover_goal()
                    '''
                  

    def aim_car(self, target_x, target_y):
        angle_between_bot_and_target = math.atan2(target_y - self.bot_pos.y, target_x - self.bot_pos.x)
        angle_to_target = angle_between_bot_and_target - self.bot_yaw
        self.controller.handbrake = abs(angle_to_target) > self.POWERSLIDE_ANGLE
        # Correct the values
        if angle_to_target < -math.pi:
            angle_to_target += 2 * math.pi
        if angle_to_target > math.pi:
            angle_to_target -= 2 * math.pi
          
        if angle_to_target < radians(-20):
            self.controller.steer = -1
        elif angle_to_target < radians(-5) and angle_to_target >= radians(-20):
            self.controller.steer = -.5
        elif angle_to_target > radians(20):
            self.controller.steer = 1
        elif angle_to_target <= radians(20) and angle_to_target > radians(5):
            self.controller.steer = .5
        else:
             self.controller.steer = 0
    
    def set_speed(self):
        if self.bot_to_ball < 1000 and r_velocity(self.bot_vel, self.ball_vel) < 200 and self.behind_ball():
            self.controller.throttle = 0
        else:
            self.controller.throttle = 1

    def set_boost(self, is_super_sonic):
        if is_super_sonic:
            self.controller.boost = False
        elif self.bot_to_ball > self.DISTANCE_FROM_BALL_TO_BOOST:
            self.controller.boost = True
        if self.ball_pos.x == 0 and self.ball_pos.x == 0: #kickoff
            self.aim_car(self.ball_pos.x, self.ball_pos.x)
            self.controller.boost = True

    def check_for_dodge(self):
        if self.bot_to_ball < self.DISTANCE_TO_DODGE and self.ball_pos.z < self.DODGE_HEIGHT: # and self.behind_ball():
            self.should_dodge = True

        if self.should_dodge and time.time() > self.next_dodge_time:
            self.controller.jump = True
            self.controller.pitch = -1

            if self.on_second_jump:
                self.on_second_jump = False
                self.should_dodge = False
            else:
                self.on_second_jump = True
                self.next_dodge_time = time.time() + self.DODGE_TIME

    def cover_goal(self):
        if self.team == 1:
            self.aim_car(0, 4900)
        else:
            self.aim_car(0, -4900)

    def behind_ball(self):
    	return self.bot_pos.y < self.ball_pos.y

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Update game data variables
        self.bot_yaw = packet.game_cars[self.team].physics.rotation.yaw
        self.bot_pos = packet.game_cars[self.index].physics.location
        self.bot_vel = packet.game_cars[self.index].physics.velocity
        self.ball_pos = packet.game_ball.physics.location
        self.ball_vel = packet.game_ball.physics.velocity
        self.bot_to_ball = distance(self.bot_pos.x, self.bot_pos.y, self.ball_pos.x, self.ball_pos.y)
        cars = packet.game_cars

        self.controller.jump = 0
        self.rotate(cars)
        self.set_boost(packet.game_cars[self.index].is_super_sonic)
        self.check_for_dodge()
        #self.set_speed()
        self.controller.throttle = 1
        return self.controller