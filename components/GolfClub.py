import pygame
import init.Setup as setup

class GolfClub:
    def __init__(self, golfClubSetup: setup.GolfClubSetup):
        self._width = golfClubSetup.width
        self._height = golfClubSetup.height
        self._distance = golfClubSetup.distance
        self._swing_power = golfClubSetup.swing_power
        self._club_color = golfClubSetup.color
        self._current_club_position = golfClubSetup.initial_position
        self._previous_club_position = golfClubSetup.initial_position

    def set_current_club_position(self, position):  self._current_club_position = position
    def set_previous_club_position(self, position): self._previous_club_position = position

    def get_current_club_position(self): return self._current_club_position
    def get_previous_club_position(self): return self._previous_club_position
    
    def get_width(self):       return self._width
    def get_height(self):      return self._height
    def get_distance(self):    return self._distance   
    def get_swing_power(self): return self._swing_power
    
    def draw_golf_stick(self, screen):
        handle_x = self.get_current_club_position().x - self._width // 2 - self._distance
        handle_y = self.get_current_club_position().y - self._height // 2
        pygame.draw.rect(
            screen,
            self._club_color,
            pygame.Rect(handle_x, handle_y, self._width, self._height)
        )

    def update_club_position(self, x_coordinate, z_coordinate, screen_height, screen_width):
        club_position = self.get_current_club_position()
        club_position.x = min(max(club_position.x + x_coordinate * 5, 0), screen_width)
        club_position.y = min(max(club_position.y + z_coordinate * 5, 0), screen_height)
        self.set_current_club_position(club_position)