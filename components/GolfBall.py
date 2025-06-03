import pygame
import init.Setup as setup

class GolfBall:
    def __init__(self, golfBallSetup: setup.GolfBallSetup):    
        self._screen_height = golfBallSetup.screen_height
        self._screen_width = golfBallSetup.screen_width    
        self._ball_position = golfBallSetup.initial_position
        self._ball_velocity = golfBallSetup.initial_velocity
        self._ball_radius = golfBallSetup.radius
        self._friction = golfBallSetup.friction
        self._min_speed = golfBallSetup.min_speed
        self._color = golfBallSetup.color_white

    def get_ball_position(self):  return self._ball_position
    def get_ball_velocity(self):  return self._ball_velocity
    def get_ball_radius(self):    return self._ball_radius
    def get_ball_friction(self):  return self._friction
    def get_ball_min_speed(self): return self._min_speed
    def get_screen_height(self):  return self._screen_height   
    def get_screen_width(self):   return self._screen_width
    
    def set_ball_position(self, position): self._ball_position = position
    def set_ball_velocity(self, velocity): self._ball_velocity = velocity

    def is_moving(self): return self._ball_velocity.length_squared() > self._min_speed
    
    def draw(self, screen, camera_x):
        screen_ball_pos = self.get_ball_position() - pygame.Vector2(camera_x, 0)
        pygame.draw.circle(screen, self._color, (int(screen_ball_pos.x), int(screen_ball_pos.y)), self.get_ball_radius())
    