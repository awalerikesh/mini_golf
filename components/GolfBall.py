import pygame
import init.Setup as setup

"""Class to represent the golf ball, handle its movement, and detect collisions."""
class GolfBall:

    """Initializes the golf ball with properties from the setup object."""
    def __init__(self, golfBallSetup: setup.GolfBallSetup):    
        self._screen_height = golfBallSetup.screen_height
        self._screen_width = golfBallSetup.screen_width    
        self._ball_position = golfBallSetup.initial_position
        self._ball_velocity = golfBallSetup.initial_velocity
        self._ball_radius = golfBallSetup.radius
        self._friction = golfBallSetup.friction
        self._min_speed = golfBallSetup.min_speed
        self._color = golfBallSetup.color_white

    """Getter"""
    def get_ball_position(self):
        return self._ball_position
    
    def get_ball_velocity(self):
        return self._ball_velocity
     
    def get_ball_radius(self):
        return self._ball_radius
    
    """Setter"""
    def set_ball_position(self, position):
        self._ball_position = position

    def set_ball_velocity(self, velocity):
        self._ball_velocity = velocity

    """Check if the ball is moving or has stopped"""
    def is_moving(self):
        return self._ball_velocity.length_squared() > self._min_speed
    
    """Draws the ball on the given screen."""
    def draw(self, screen, camera_x):
        screen_ball_pos = self.get_ball_position() - pygame.Vector2(camera_x, 0)
        pygame.draw.circle(screen, self._color, (int(screen_ball_pos.x), int(screen_ball_pos.y)), self.get_ball_radius())
    
    """Updates the ball's position and handles friction, boundaries, and collisions."""
    def update(self, screen, obstacles, camera_x):
        if self._ball_velocity.length() > 0.1:
            self._apply_friction()   # Apply friction to the ball
            self._ball_position += self._ball_velocity # Move the ball
            self.draw(screen, camera_x)   # Draw the updated ball position
        else:
            self._stop_ball() # If ball velocity is too small, stop the ball


        # Check and handle boundary collisions (edges of the screen)
        self._check_and_handle_boundaries()

        # Check and handle collisions with barriers (obstacles)
        self._handle_barrier_collision(obstacles)

    """Applies friction to the ball's velocity and stops the ball if the speed is below the minimum."""
    def _apply_friction(self):
        self._ball_velocity *= self._friction
        if self._ball_velocity.length() < self._min_speed:
            print("Ball stopped.")
            self._ball_velocity = pygame.Vector2(0, 0)

    """Stops the ball by setting its velocity to zero."""
    def _stop_ball(self):
        self._ball_velocity = pygame.Vector2(0, 0)

    """Checks for collisions with obstacles (barriers) and adjusts the ball's velocity upon impact."""
    def _handle_barrier_collision(self, obstacles):
        for barrier in obstacles.get_barriers():
            ball_rect = pygame.Rect(self._ball_position.x - self._ball_radius, self._ball_position.y - self._ball_radius, self._ball_radius * 2, self._ball_radius * 2)
            if barrier.rect.colliderect(ball_rect):
                if barrier.rect.width > barrier.rect.height:
                    self._ball_velocity.y *= -1
                else:
                    self._ball_velocity.x *= -1
    
    """Checks and handles boundary collisions (edges of the screen)."""
    def _check_and_handle_boundaries(self):
        self._check_horizontal_boundaries()
        self._check_vertical_boundaries()

    """Checks if the ball has hit the horizontal boundaries (left or right)."""
    def _check_horizontal_boundaries(self):
        if self._ball_position.x - self._ball_radius < 0 or self._ball_position.x + self._ball_radius > 5000:
            self._ball_velocity.x *= -1
            self._ball_position.x = max(self._ball_radius, min(self._ball_position.x, 5000 - self._ball_radius)) 

    """Checks if the ball has hit the vertical boundaries (top or bottom)."""
    def _check_vertical_boundaries(self, ):
        if self._ball_position.y - self._ball_radius < 0 or self._ball_position.y + self._ball_radius > self._screen_height:
            self._ball_velocity.y *= -1
            self._ball_position.y = max(self._ball_radius, min(self._ball_position.y, self._screen_height - self._ball_radius))
