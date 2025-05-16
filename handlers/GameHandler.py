import components as gc
import pygame

class GameHandler:
    def __init__(self, ball: gc.GolfBall, club: gc.GolfClub, hole: gc.GolfHole, obstacles: gc.Obstacles):
        self._ball: gc.GolfBall = ball
        self._club: gc.GolfClub = club
        self._hole: gc.GolfHole = hole
        self._obstacles: gc.Obstacles = obstacles
    
    """Check if the club strikes the ball"""
    def check_strike(self, club_position, camera_x):
        # Calculate screen position of the ball (adjusted to represent the front side)
        screen_ball_position = self._ball.get_ball_position() + pygame.Vector2(self._ball.get_ball_radius() * 2, 0) - pygame.Vector2(camera_x, 0)

        # Vector from club to ball
        direction_to_ball = screen_ball_position - club_position
        distance_to_ball = direction_to_ball.length()

        # Check if the club is close enough and approaching from the left
        is_close_enough = distance_to_ball <= self._ball.get_ball_radius() + self._club.get_width() // 2
        is_from_left = club_position.x <= screen_ball_position.x

        if is_close_enough and is_from_left:
            return True, direction_to_ball

        return False, direction_to_ball
    
    """Calculate the ball velocity using the previous and current ball position"""
    def calculate_ball_velocity(self, prev_club_position, curr_club_position, direction_to_ball):
        speed = (curr_club_position - prev_club_position).length()
        strike_power = min(speed, self._club.get_swing_power())
        direction = direction_to_ball.normalize()
        ball_velocity = direction * strike_power
        self._ball.set_ball_velocity(ball_velocity)
    
    """Updates the ball's position and handles friction, boundaries, and collisions."""
    def update_ball(self, screen, camera_x):
        if self._ball.get_ball_velocity().length() > 0.1:
            self._apply_friction()   # Apply friction to the ball
            ball_postion = self._ball.get_ball_position()
            ball_velocity = self._ball.get_ball_velocity()
            ball_position += ball_velocity # Move the ball
            self._ball.set_ball_position(ball_postion)
            self._ball.draw(screen, camera_x)   # Draw the updated ball position
        else:
            self._stop_ball() # If ball velocity is too small, stop the ball


        # Check and handle boundary collisions (edges of the screen)
        self._check_and_handle_boundaries()

        # Check and handle collisions with barriers (obstacles)
        self._handle_barrier_collision()

    def is_ball_moving(self):
        return self._ball.is_moving()
    
    """Applies friction to the ball's velocity and stops the ball if the speed is below the minimum."""
    def _apply_friction(self):
        self._ball.get_ball_velocity() *= self._ball.get_ball_friction()
        if self._ball.get_ball_velocity.length() < self._ball.get_ball_min_speed():
            print("Ball stopped.")
            self._ball.set_ball_velocity(pygame.Vector2(0, 0)) 

    """Stops the ball by setting its velocity to zero."""
    def _stop_ball(self):
        self._ball.set_ball_velocity(pygame.Vector2(0, 0))

    """Checks for collisions with obstacles (barriers) and adjusts the ball's velocity upon impact."""
    def _handle_barrier_collision(self):
        for barrier in self._obstacles.get_barriers():
            ball_rect = pygame.Rect(self._ball.get_ball_position().x - self._ball.get_ball_radius(), self._ball.get_ball_position().y - self._ball.get_ball_radius(), self._ball.get_ball_radius() * 2, self._ball.get_ball_radius() * 2)
            if barrier.rect.colliderect(ball_rect):
                ball_velocity = self._ball.get_balekvelocity()
                if barrier.rect.width > barrier.rect.height:
                    ball_velocity.y *= -1
                else:
                    ball_velocity.x *= -1
                self._ball.set_ball_velocity(ball_velocity)
    
    """Checks and handles boundary collisions (edges of the screen)."""
    def _check_and_handle_boundaries(self):
        self._check_horizontal_boundaries()
        self._check_vertical_boundaries()

    """Checks if the ball has hit the horizontal boundaries (left or right)."""
    def _check_horizontal_boundaries(self):
        ball_velocity = self._ball.get_ball_velocity()
        if self._ball.get_ball_position().x - self._ball.get_ball_radius() < 0 or self._ball.get_ball_position().x + self._ball.get_ball_radius() > 5000:
            ball_velocity.x *= -1
            self._ball.get_ball_position().x = max(self._ball.get_ball_radius(), min(self._ball.get_ball_position().x, 5000 - self._ball.get_ball_radius())) 
        self._ball.set_ball_velocity(ball_velocity)

    """Checks if the ball has hit the vertical boundaries (top or bottom)."""
    def _check_vertical_boundaries(self):
        ball_velocity = self._ball.get_ball_velocity()
        if self._ball.get_ball_position().y - self._ball.get_ball_radius() < 0 or self._ball.get_ball_position().y + self._ball.get_ball_radius() > self._ball.get_screen_height():
            ball_velocity.x *= -1
            self._ball.get_ball_position().y = max(self._ball.get_ball_radius(), min(self._ball.get_ball_position().y, self._ball.get_screen_height() - self._ball.get_ball_radius()))
        self._ball.set_ball_velocity(ball_velocity)

    def draw_ball(self):
        self._ball.draw()

    def draw_club(self, position):
        self._club.draw_golf_stick(position)