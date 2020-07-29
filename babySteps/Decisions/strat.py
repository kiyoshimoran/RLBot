from Decisions.info import MyInfo
from Decisions.challengeGame import ChallengeGame
from Actions.Kickoff import kickoff
from Actions.Chase import chase
from Actions.Action import Action
from Actions.Shadow import shadow
from Actions.Challenge import challenge
from util.vec import Vec3

CHALLENGE_TIME = 0.4

class Strategy:

    LOW_BOOST = 20

    def __init__(self, info: MyInfo):
        self.info = info
        #self.challengeGame = ChallengeGame(car, info.ball_path)
        self.rushing = True
        self.airGame = True
        self.drift_angle = 37
        self.drift_dist = 3000



    def chooseAction(self, info: MyInfo) -> Action:
        '''
        if self.info.kickoff_pause:
            return kickoff(self.car, self.info)
        else:
        '''
        ball_pos = Vec3(self.info.ball_path[0].physics.location)
        cg = ChallengeGame(self.info.car, self.info)
        o_cg = ChallengeGame(self.info.opp_car, self.info)
        my_ttb = cg.get_time_to_loc(ball_pos)
        op_ttb = o_cg.get_time_to_loc(ball_pos)
        #print("\nmy ttb: {}, opp ttb: {}\n\n".format(my_ttb, op_ttb))
        #print(cg.get_time_to_loc(cg.challenge_loc))
        if can_challenge(my_ttb, op_ttb):
            return challenge(info)
        elif my_ttb < op_ttb:
            return chase(cg.car, self.info, cg.challenge_loc)
        # grab boost if low and have time
        #elif self.car.boost < LOW_BOOST
        else:
            return shadow(self.info)

def can_challenge(my_ttb, op_ttb):
    '''
    ball_loc = Vec3(self.info.ball_path[0].physics.location)
    my_ttb = self.cg.get_time_to_loc(ball_loc)
    op_ttb = self.o_cg.get_time_to_loc(ball_loc)
    '''
    if op_ttb - CHALLENGE_TIME > my_ttb:
        return True
    return False
