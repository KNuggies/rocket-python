from math import pi

import pygame
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3

from shots.shots import Shot

class MyBot(BaseAgent):

    # TODO:
    # Flip Indicator

    def __init__(self, name, team, index):
        super().__init__(name, team, index)

        self.reset_shot = False

        # Use pygame to monitor (and later log) player input
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def initialize_agent(self):
        print("Called: initialize_agent")

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """

        # Set player index (assumes one bot, one player, on different teams)
        if self.index == 0:
            player_index = 1
        else:
            player_index = 0

        # Monitor controller input to reset shot
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 8: # R3 for reset
                    self.reset_shot = True

        # Define Shot
        if self.reset_shot:
            self.reset_shot = False
            shot = Shot(player_index, True)
            state = GameState(
                ball = shot.ball,
                cars = shot.cars
            )
            self.set_game_state(state)

        controls = SimpleControllerState()

        return controls
