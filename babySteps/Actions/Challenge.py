from Actions.Action import Action
from Drawing.Drawing import DrawingTool
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.sequence import StepResult
from util.orientation import Orientation, relative_location
from util.vec import Vec3
from Decisions.info import MyInfo, Car
from Decisions.challengeGame import ChallengeGame

from math import pi 
from math import cos

FLIP_TIME = 0.05


class challenge(Action):
	
	def __init__(self, info) -> SimpleControllerState:
		super().__init__()
		self.info = info
		self.last_touch = info.last_touch.time_seconds
		self.car = info.car
		self.start_time = info.seconds_elapsed
		self.cg = ChallengeGame(self.info.car, self.info)
		self.o_cg = ChallengeGame(self.info.opp_car, self.info)
		self.name = "Challenge"

	def tick(self, info : MyInfo):
		print("first {}".format(self.done))
		target = Vec3(self.info.ball_path[0].physics.location)
		relative = relative_location(Vec3(self.info.car.loc), Orientation(self.car.rot), target)
		if self.start_time + FLIP_TIME > info.seconds_elapsed:
			print("first jump")
			self.controls.jump = True
			#self.start_time = self.info.seconds_elapsed
		elif self.start_time + 2 * FLIP_TIME > self.info.seconds_elapsed:
			print("not jump")
			self.controls.jump = False
			self.controls.yaw = cos(relative.y / relative.x)
		elif self.start_time + 3 * FLIP_TIME > info.seconds_elapsed:
			print("second jump")
			if relative.x > 0:
				self.controls.pitch = -1
			else:
				self.controls.pitch = 1
			self.controls.yaw = cos(relative.y / relative.x)
			self.controls.jump = True
		if self.new_touch: # or self.start_time + 1.1 < info.seconds_elapsed:
			#print("start time: {}, current time: {}".format(self.start_time, info.seconds_elapsed))
			self.done = True
		print(self.done)
		return self.controls