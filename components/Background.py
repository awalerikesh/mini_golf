import pygame
import math
import init.Setup as setup

class Background: 
    def __init__(self, backgroundSetup: setup.BackgroundSetup):
        self._screen =  pygame.display.set_mode(size=(backgroundSetup.width, backgroundSetup.height))
        self._width = backgroundSetup.width
        self._height = backgroundSetup.height
        self._sky_color = backgroundSetup.sky_color
        self._hill_color = backgroundSetup.hill_color

    def _draw_sky(self, camera_x):
        sky_scroll = -camera_x * 0.2
        for i in range(6):
            pygame.draw.rect(self._screen, self._sky_color, (sky_scroll + i * self._width, 0, self._width, self._height))

    def _draw_mountain(self, camera_x):
        mountain_scroll = -camera_x * 0.5
        for i in range(8):
            pygame.draw.polygon(self._screen, (100, 100, 100), [
                (mountain_scroll + i * self._width + 100, 400),
                (mountain_scroll + i * self._width + 300, 200),
                (mountain_scroll + i * self._width + 500, 400)
            ])

    def _draw_hill(self, camera_x):
        hill_scroll = -camera_x * 1    
        for i in range(8):
            pygame.draw.arc(self._screen, self._hill_color, (hill_scroll + i * self._width - 300, 300, 600, 400), math.pi, 2 * math.pi, 0)
            pygame.draw.rect(self._screen, self._hill_color, (hill_scroll + i * self._width, 400, self._width, self._height))

    def draw_background(self,camera_x):
        self._draw_sky(camera_x)
        self._draw_mountain(camera_x)
        self._draw_hill(camera_x)
