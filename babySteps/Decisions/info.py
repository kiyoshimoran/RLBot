from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.utils.structures.game_data_struct import GameInfo, Rotator, PlayerInfo

from util.vec import Vec3


class Goal:

    WIDTH = 1784.0
    HEIGHT = 640.0
    DISTANCE = 5120.0

    def __init__(self, team):
        sign = -1 if team == 0 else 1
        self.center = Vec3(0, sign * Goal.DISTANCE, 0)
        self.team = team

    def inside(self, pos) -> bool:
        return pos[1] < -Goal.DISTANCE if self.team == 0 else pos[1] > Goal.DISTANCE


class MyInfo(GameInfo):

    def __init__(self, team, index):
        super().__init__()
        self.team = team
        self.index = index
        self.my_goal = Goal(team)
        self.their_goal = Goal(1 - team)
        self.about_to_score = False
        self.about_to_be_scored_on = False
        self.time_of_goal = -1
        self.last_touch = None
        self.ball_path = []
        self.seconds_elapsed
        self.car = Car()
        self.opp_car = Car()
        #self.large_boost_pads: List[Pad] = []

    def read_packet(self, packet: GameTickPacket, bp):
        self.last_touch = packet.game_ball.latest_touch
        self.ball_path = bp
        self.seconds_elapsed = packet.game_info.seconds_elapsed
        self.car.updateCar(packet, self.index)
        self.opp_car.updateCar(packet, 1 - self.index)



    def get_opp_car(self, packet):
        for car in packet.game_cars:
            if car.team != self.team:
                return car

class Car():

    def __init__(self):
        self.vel = None
        self.loc = None
        self.rot = None

    def updateCar(self, packet : GameTickPacket, index):
        car = packet.game_cars[index]
        phys = car.physics
        self.vel = Vec3(phys.velocity)
        self.loc = Vec3(phys.location)
        self.rot = phys.rotation
        self.boost = car.boost
        self.jumped = car.jumped

class Ball():
    def __init__(self):
        self.vel = None
        self.loc = None
        self.rot = None
        self.path = None