import pygame
import init.Setup as setup
from .GolfBall import GolfBall

class GolfClub:
    def __init__(self, golfClubSetup: setup.GolfClubSetup):
        self._width = golfClubSetup.width
        self._height = golfClubSetup.height
        self._screen =  pygame.display.set_mode(size=(golfClubSetup.width, golfClubSetup.height))
        self._distance = golfClubSetup.distance
        self._swing_power = golfClubSetup.swing_power
        self._club_color = golfClubSetup.color

    """Draws the golf club as a rectangle on the given surface at the specified start position."""
    def draw_golf_stick(self, position):
        handle_x = position.x - self._width // 2 - self._distance
        handle_y = position.y - self._height // 2
        pygame.draw.rect(
            self._screen,
            self._club_color,
            pygame.Rect(handle_x, handle_y, self._width, self._height)
        )

    """Update the club position using the gyroscope data"""
    def update_club_position(self, club_position, x_coordinate, z_coordinate, screen_height, screen_width):
        club_position.x = min(max(club_position.x - x_coordinate * 5, 0), screen_width//3)
        club_position.y = min(max(club_position.y + z_coordinate * 5, 0), screen_height)
        return club_position

    """Check if the club strikes the ball"""
    def check_strike(self, club_position, ball: GolfBall, camera_x):
        # Calculate screen position of the ball (adjusted to represent the front side)
        screen_ball_position = ball.get_ball_position() + pygame.Vector2(ball.get_ball_radius() * 2, 0) - pygame.Vector2(camera_x, 0)

        # Vector from club to ball
        direction_to_ball = screen_ball_position - club_position
        distance_to_ball = direction_to_ball.length()

        # Check if the club is close enough and approaching from the left
        is_close_enough = distance_to_ball <= ball.get_ball_radius() + self._width // 2
        is_from_left = club_position.x <= screen_ball_position.x

        if is_close_enough and is_from_left:
            return True, direction_to_ball

        return False, direction_to_ball

    """Calculate the ball velocity using the previous and current ball position"""
    def calculate_ball_velocity(self, prev_club_position, curr_club_position, direction_to_ball, ball: GolfBall):
        speed = (curr_club_position - prev_club_position).length()
        strike_power = min(speed, self._swing_power)
        direction = direction_to_ball.normalize()
        ball_velocity = direction * strike_power
        ball.set_ball_velocity(ball_velocity)

