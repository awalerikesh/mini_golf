import pygame
import init.Setup as setup

class GolfHole:
    def __init__(self, golfHoleSetup: setup.GolfHoleSetup):
        self._screen = pygame.display.set_mode(size=(golfHoleSetup.width, golfHoleSetup.height))
        self._height = golfHoleSetup.height
        self._hole_radius = golfHoleSetup.hole_radius
        self._hole_position = golfHoleSetup.hole_position
        self._outline_thickness = golfHoleSetup.outline_thickness
        self._screen_offset = golfHoleSetup.screen_offset
        self._color_black = golfHoleSetup.color_black
        self._color_white = golfHoleSetup.color_white

    def draw_hole(self, camera_x):
        screen_pos = self._hole_position - pygame.Vector2(camera_x, 0) + self._screenOffset
        center = (int(screen_pos.x), int(screen_pos.y))
        pygame.draw.circle(self._screen, self._color_black, center, self._hole_radius + self._outline_thickness)
        pygame.draw.circle(self._screen, self._color_white, center, self._hole_radius)