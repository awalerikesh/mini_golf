import components as gc
import pygame
from .Setup import (
    create_background_setup, 
    create_golf_ball_setup, 
    create_golf_club_setup, 
    create_golf_hole_setup, 
    create_obstacles_setup, 
    ScreenSetup, 
    Colors,
    FontSetup
)

start_time = pygame.time.get_ticks()
font = pygame.font.SysFont(None, 36)

def game_initialization():

    screen_cfg = ScreenSetup()
    colors = Colors()
    background = gc.Background(create_background_setup(screen_cfg, colors))  
    golfClub = gc.GolfClub(create_golf_club_setup(screen_cfg, colors))
    obstacles = gc.Obstacles(create_obstacles_setup(screen_cfg, colors))
    golfBall = gc.GolfBall(create_golf_ball_setup(screen_cfg, colors))
    golfHole = gc.GolfHole(create_golf_hole_setup(screen_cfg, colors))
    screen = pygame.display.set_mode((screen_cfg.width, screen_cfg.height))

    return {
        "screen": screen,
        "background": background,
        "club": golfClub,
        "obstacles": obstacles,
        "ball": golfBall,
        "hole": golfHole,
        "screen_height": screen_cfg.height,
        "screen_width": screen_cfg.width,
        "camera_x": 0,
        "clock": pygame.time.Clock(),
        "game_finished": False,
        "screen_ball_position": golfBall.get_ball_position()
    }

def screen_blit(screen):
    colors = Colors()
    font_setup = FontSetup()
    current_time = (pygame.time.get_ticks() - start_time) / 1000.0
    screen.blit(font_setup.text_setup.render("Press R to Restart", True, colors.white), (10, 10))
    screen.blit(font_setup.text_setup.render(f"Time: {current_time:.2f}s", True, colors.white), (10, 50))