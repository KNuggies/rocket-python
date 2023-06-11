from math import pi, atan2, sqrt, sin, cos
import random

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator


# Transform Pop Aerial to various start locations
# Shot Dashboard
# Reset Shot on Bounce
# Track the number of tries

# TODO: Create separate file for Debug class
class Debug:
    def __init__(self):
        pass

    def print_angle(self, ang: float, name: str = 'angle'):
        print(f'{name}: {(180*ang/pi):.2f} degrees')

    def print_dist(self, dist: float, name: str = 'distance'):
        print(f'{name}: {dist:.2f} uu')

debug = Debug()

"""
Pop Aerial Shot
"""
class Shot:
    def __init__(self, player_index: int, transform: bool = False):
        self.player_index = player_index
        self.ball = BallState(
                    physics=Physics(
                        location = Vector3(0.0, -1800.0, 1000.0),
                        velocity = Vector3(0.0, -1000.0, 0.0),
                        rotation = Rotator(0, 0, 0),
                        angular_velocity = Vector3(0, 0, 0)
                    )
                )
        self.cars = {
            self.player_index: CarState(
                physics=Physics(
                    location = Vector3(0.0, -5000.0, 17.02),
                    velocity = Vector3(0.0, 0.0, -0.0001),
                    rotation = Rotator(0, pi/2, 0), # (pitch, yaw, roll) in car fame
                    angular_velocity = Vector3(0, 0, 0)
                ),
                boost_amount=100.0
            )
        }

        if transform:
            self.transform_location()

    def transform_location(self):
        # TODO Deal with corner cases (car in the corner)
        
        dx = random.randint(-3000, 3000)
        dy = random.randint(0, 3000)

        print("Perform Transform")
        # Get initial values
        ball_loc = self.ball.physics.location
        ball_vel = self.ball.physics.velocity
        car_loc = self.cars[self.player_index].physics.location
        car_rot = self.cars[self.player_index].physics.rotation
        h_dist_to_ball = sqrt((car_loc.x - ball_loc.x)**2 + (car_loc.y - ball_loc.y)**2)
        ball_vel_mag = sqrt(ball_vel.x**2 + ball_vel.y**2)
        net_x = 0
        net_y = 5120 # TODO Adjust for player on orange team (currently assumes blue team)

        # Transform Shot
        car_loc.x += dx
        car_loc.y += dy

        yaw = atan2(-(car_loc.x - net_x), -(car_loc.y - net_y))
        car_rot.yaw -= yaw
        debug.print_angle(car_rot.yaw, 'yaw')
        ball_loc.x = car_loc.x + h_dist_to_ball*sin(yaw)
        ball_loc.y = car_loc.y + h_dist_to_ball*cos(yaw)

        ball_vel.x = -ball_vel_mag*sin(yaw)
        ball_vel.y = -ball_vel_mag*cos(yaw)

        # Assing transformed values
        self.cars[self.player_index].physics.location = car_loc
        self.cars[self.player_index].physics.rotation = car_rot
        self.ball.physics.location = ball_loc
        self.ball.physics.velocity = ball_vel
