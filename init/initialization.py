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
    Colors,
    FontSetup
)

start_time = pygame.time.get_ticks()
font = pygame.font.SysFont(None, 36)

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

def screen_blit_time(screen, start_time):
    colors = Colors()
    font_setup = FontSetup()
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    screen.blit(font_setup.text_setup.render("Press R to Restart", True, colors.white), (10, 10))
    screen.blit(font_setup.text_setup.render("Press C to Reset the Club", True, colors.white), (10, 50))
    screen.blit(font_setup.text_setup.render(f"Time: {elapsed_time:.2f}s", True, colors.white), (10, 90))

def screen_blit_game_finished(screen):
    font_setup = FontSetup()
    colors = Colors()
    print(ScreenSetup.width)
    completion_time = (pygame.time.get_ticks()) / 1000.0
    screen.blit(font_setup.text_setup.render("Game Set and Done! Press R to Restart", True, colors.white), (10, 100))
    screen.blit(font_setup.text_setup.render(f"Time: {completion_time:.2f} seconds", True, colors.white), (10, 150))