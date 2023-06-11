from math import pi

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

from shots.shots import Shot

from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()
        self.has_jumped = False

    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())
        print("Called: initialize_agent")

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """

        # Gather some information about our car and the ball
        if self.index == 0:
            player_index = 1
        else:
            player_index = 0
        
        bot_car = packet.game_cars[self.index]
        # packet.game_cars[self.index].physics.location.z = 500
        
        player_car = packet.game_cars[player_index]

        player_location = Vec3(player_car.physics.location)
        # print(f'Player Location: <{player_location.x:8.2f}, {player_location.y:8.2f}, {player_location.z:8.2f}>')
        
        ball_location = Vec3(packet.game_ball.physics.location)
        # print(f'Ball Location: <{ball_location.x:8.2f}, {ball_location.y:8.2f}, {ball_location.z:8.2f}>')
        
        # TODO:
        # Create Debug Info for Printing messages
        # Flip Indicator
        # Find better game state to reset shot to enable replays

        if not self.has_jumped and player_location.z > 100:
            self.has_jumped = True

        # Define Shot
        if not packet.game_info.is_round_active and self.has_jumped:
            self.has_jumped = False
            # print("Not active (includes pause state)")
            self.renderer.draw_string_3d(player_location, 3, 3, 'Ball Reset', self.renderer.white())
            # Set Shot
            shot = Shot(player_index, True)
            state = GameState(
                ball = shot.ball,
                cars = shot.cars
            )
            self.set_game_state(state)

        controls = SimpleControllerState()

        return controls
