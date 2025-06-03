import pygame
import random
import init.Setup as setup

class Obstacles:
    def __init__(self, obstacleSetup: setup.ObstaclesSetup):
        self._screen = pygame.display.set_mode(size=(obstacleSetup.width, obstacleSetup.height))
        self._height = obstacleSetup.height
        self._barriers = obstacleSetup.barriers
        self._whirlpools = obstacleSetup.whirlpools
        self._barrier_color = obstacleSetup.barrier_color
        self._whirlpool_color = obstacleSetup.whirlpool_color

    def get_barriers(self):   return self._barriers
    def get_whirlpools(self): return self._whirlpools

    def _draw_barriers(self,camera_x):
        for barrier in self._barriers:
            rect = barrier.rect.copy()
            rect.x -= camera_x
            pygame.draw.rect(self._screen, self._barrier_color, rect)

    def _draw_whirlpools(self, camera_x):
        for wp in self._whirlpools:
            center_screen = wp.center - pygame.Vector2(camera_x, 0)
            for r in range(0, wp.radius, 5):
                pygame.draw.circle(self._screen, self._whirlpool_color, (int(center_screen.x), int(center_screen.y)), r, 1)

    def _move_barriers(self):
        for barrier in self._barriers:
            if barrier.direction == "up":
                barrier.rect.y -= barrier.speed
            else:
                barrier.rect.y += barrier.speed
            if barrier.rect.y < 0:
                barrier.rect.y = 0
                barrier.direction = "down"
            if barrier.rect.y > self._height - barrier.rect.height:
                barrier.rect.y = self._height - barrier.rect.height
                barrier.direction = "up"

    def apply_whirlpool_force(self, ballVelocity, ball_position):
        for wp in self._whirlpools:
            dist = (ball_position - wp.center).length()
            if dist < wp.radius:
                direction = (wp.center - ball_position).normalize()
                perpendicular = pygame.Vector2(-direction.y, direction.x)
                ballVelocity += direction * 0.1 + perpendicular * 0.2
        return ballVelocity

    def draw(self, camera_x):
        self._draw_barriers(camera_x)
        self._move_barriers()
        self._draw_whirlpools(camera_x)