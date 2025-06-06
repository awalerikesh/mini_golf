import components as gc
import handlers as handler
import pygame
from .Setup import (
    create_background_setup, 
    create_golf_ball_setup, 
    create_golf_club_setup, 
    create_golf_hole_setup, 
    create_obstacles_setup, 
    ScreenSetup, 
    Colors
)

def game_initialization():
    screen_cfg = ScreenSetup()
    colors = Colors()
    background = gc.Background(create_background_setup(screen_cfg, colors))  
    club = gc.GolfClub(create_golf_club_setup(screen_cfg, colors))
    obstacles = gc.Obstacles(create_obstacles_setup(screen_cfg, colors))
    ball = gc.GolfBall(create_golf_ball_setup(screen_cfg, colors))
    hole = gc.GolfHole(create_golf_hole_setup(screen_cfg, colors))
    screen = pygame.display.set_mode((screen_cfg.width, screen_cfg.height))
    #screen = pygame.display.set_mode((screen_cfg.width, screen_cfg.height),pygame.FULLSCREEN)
    screen_ball_position = ball.get_ball_position()
    club_position = screen_ball_position - pygame.Vector2(20, 0)
    club.set_current_club_position(club_position)
    prev_club_position = club_position.copy()
    club.set_previous_club_position(prev_club_position)
    
    game_handler = handler.GameHandler(background, screen, ball, club, hole, obstacles, screen_cfg.width, screen_cfg.height, screen_cfg.world_width)
    return game_handler