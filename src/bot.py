from math import pi

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState

# from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.game_state_util import (
    GameState,
)  # , BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

# from util.ball_prediction_analysis import find_slice_at_time
# from util.boost_pad_tracker import BoostPadTracker
# from util.drive import steer_toward_target
# from util.sequence import Sequence, ControlStep
# from util.vec import Vec3

from controller import Controller, RESET_SHOT_BUTTON
from shots.shots import Shot


class MyBot(BaseAgent):
    # TODO:
    # Flip Indicator

    def __init__(self, name, team, index):
        super().__init__(name, team, index)

        self.controller = Controller()
        self.reset_shot = False

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

        print("Double Jumped: ", packet.game_cars[player_index].double_jumped)
        print("Has Wheel Contact: ", packet.game_cars[player_index].has_wheel_contact)
        print("Jumped: ", packet.game_cars[player_index].jumped)
        # When jump turned to true and back to false without being on the ground, a flip reset hit
        # Could check proximity to ball etc. Not sure how much it matters (diff for ceiling reset)``
        # Create two state checks: Flip reset and Ceiling Reset

        # Check controller and reset if needed
        if RESET_SHOT_BUTTON in self.controller.get_events():
            self.reset_shot = True

        # Define Shot
        if self.reset_shot:
            self.reset_shot = False
            shot = Shot(player_index, True)
            state = GameState(ball=shot.ball, cars=shot.cars)
            self.set_game_state(state)

        controls = SimpleControllerState()

        return controls
