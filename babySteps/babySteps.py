from rlbot.agents.base_agent import BaseAgent, GameTickPacket, SimpleControllerState
#from rlbot.utils.structures.game_data_struct import GameTickPacket
from Decisions.challengeGame import ChallengeGame
from Decisions.info import MyInfo, Car
from Decisions.strat import Strategy
from Drawing.Drawing import DrawingTool
from util.vec import Vec3
from Actions.Kickoff import kickoff
from Actions.Chase import chase
# Blue team's (0) goal is located at (0, -5120) 
# Orange (1) at (0, 5120)
# ball R = 92

from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3


import math
import time
from math import radians

kickoff_location = Vec3(0, 0, 0)

class MyBot(BaseAgent):


    def __init__(self, name, team, index):
        super().__init__(name, team, index) 
        self.action: Action = kickoff
        self.info : GameInfo = None
        self.car : Car = None
        self.boost_pad_tracker = BoostPadTracker()
        self.stat : Strategy = None
        self.action : Action = None

    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())
        self.info = MyInfo(self.team, self.index)
        self.strat = Strategy(self.info)
        self.car = Car()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """

        # Keep our boost pad info updated with which pads are currently active
        self.boost_pad_tracker.update_boost_status(packet)
        #self.info = self.info.read_packet(packet)  
        self.car.updateCar(packet, self.index)
        self.info.read_packet(packet, self.get_ball_prediction_struct().slices)
        #print("in main target: {}".format(self.get_ball_prediction_struct().slices[0].physics.location))
        #self.renderer.draw_line_3d(self.car.loc, target_location, self.renderer.white())
        #self.renderer.draw_rect_3d(target_location, 8, 8, True, self.renderer.cyan(), centered=True)
       
        #cg = ChallengeGame(self.car, bp_struct)
        
        #print(cg.get_time_to_loc(cg.challenge_loc))
        # This is good to keep at the beginning of get_output. It will allow you to continue
        # any sequences that you may have started during a previous call to get_output.
        if self.action is None:
            self.action = self.strat.chooseAction(self.info)
            
            controls = self.action.tick(self.info)
            print(controls.steer)
            return controls
        

        self.renderer.draw_string_3d(self.car.loc, 1, 1, f'Speed: {self.car.vel.length():.1f}', self.renderer.white())
        if self.action.name:
            self.renderer.draw_string_3d(self.car.loc + Vec3(0, 0, 20), 1, 1, self.action.name, self.renderer.white())
        

        if packet.game_info.is_kickoff_pause and not isinstance(self.action, kickoff):
            #self.logger.info(self.action)
            self.action = kickoff(self.car.loc)
            #print("Sequence is: {}".format(self.action))
            #print("Sequence finished: {}".format(self.action.done))
            controls = self.action.tick(self.info)
            return controls
        
        if self.action and not self.action.done:
            controls = self.action.tick(self.info)
            #print("action is: {}".format(self.action.name))
            if controls is not None:
                return controls
        
        elif self.action.done:
            print("choosing new action")
            
            self.action = self.strat.chooseAction(self.info)
            controls = self.action.tick(self.info)
            return controls

        # Gather some information about our car and the ball
        ball_location = Vec3(packet.game_ball.physics.location)

        if self.car.loc.dist(ball_location) > 1500:
            # We're far away from the ball, let's try to lead it a little bit
            ball_prediction = self.get_ball_prediction_struct()  # This can predict bounces, etc
            ball_in_future = find_slice_at_time(ball_prediction, packet.game_info.seconds_elapsed + 2)
            target_location = Vec3(ball_in_future.physics.location)
            self.renderer.draw_line_3d(ball_location, target_location, self.renderer.cyan())
        else:
            target_location = ball_location

        # Draw some things to help understand what the bot is thinking
         #self.renderer.draw_string_2d(100, 100, 1, 1, f'Ball at: {ball_location}', self.renderer.white())

        '''
        if 750 < self.car.vel.length()  < 800:
            # We'll do a front flip if the car is moving at a certain speed.
            return self.begin_front_flip(packet)
        
        #controls = self.action.controls
        controls = SimpleControllerState()
        controls.steer = steer_toward_target(self.car, target_location)
        controls.throttle = 1.0
        # You can set more controls if you want, like controls.boost.
        '''
        print("the fuck we doin here?!?!?!?")
        return controls

    def begin_front_flip(self, packet):
        # Send some quickchat just for fun
        self.send_quick_chat(team_only=False, quick_chat=QuickChatSelection.Information_IGotIt)

        # Do a front flip. We will be committed to this for a few seconds and the bot will ignore other
        # logic during that time because we are setting the action.
        self.action = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        # Return the controls associated with the beginning of the sequence so we can start right away.
        return self.action.tick(packet)

    def is_kickoff(self, ball_location, ball_velocity):
        #self.logger.info(ball_location.flat() == kickoff_location)
        #self.logger.info(ball_velocity.length() == 0)
        return ball_location.flat() == kickoff_location and ball_velocity.length() == 0


'''
class Bot(BaseAgent):
    DEVMODE = True

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.info: GameInfo = None
        self.draw: DrawingTool = None
        self.strat: Strategy = None
        self.car = None
        self.Actions: Maneuver = None
        self.controls: SimpleControllerState = SimpleControllerState()

    def initialize_agent(self):
        #self.logger.info(rlutilities.__file__)
        self.info = GameInfo(self.team)
        #for field in self.info._fields_:
        #    print(field[0], getattr(self.info, field[0]))
        self.info.set_mode("soccar")
        self.draw = DrawingTool(self.renderer)
        self.car = self.info.cars[self.index]
        self.logger.info("my index is {}".format(self.index))
        self.strat = Strategy(self.info, my_car)

    def get_output(self, packet: GameTickPacket):
        # Update game data variables
       
        if self.tick_counter < 20:
            self.tick_counter += 1
            return Input()
           

        if self.Actions is None and not self.Actions.finished:
            controls = self.Action.tick(packet)

        self.info.read_packet(packet, self.get_field_info(), self.get_ball_path())

        self.draw.draw_path(self.get_ball_path())
        challenge = ChallengeGame(self.info.cars[self.index], self.info.ball_path)

        if challenge.should_go:
            self.Action = self.strat.chooseAction(challenge, self.info.ball_path)
        self.controls = self.Action.controls
        print(self.Action)
        
        if self.info.is_kickoff():
            return self.do
        self.controls = self.action.doThing(self.info)
        
        if self.DEVMODE:
            self.Action.render(self.draw)
            challenge.render(self.draw)

        return self.controls

   
    def get_ball_path(self):
        ball_prediction = self.get_ball_prediction_struct()
        path = []
        for i in range(0, ball_prediction.num_slices):
            prediction_slice = ball_prediction.slices[i]
            loc = prediction_slice.physics.location
            path.append(loc)
        return path

'''