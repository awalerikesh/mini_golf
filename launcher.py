import pygame
import handlers.GameHandler as gh
import handlers.gyroscopeHandler as osc
import init as initialize
import sys

osc.osc_thread_start()
gh = initialize.game_initialization()
pygame.display.set_caption("Mini Golf")
pygame.init()
gh.show_welcome_screen_and_wait()
start_time = pygame.time.get_ticks()

while True:
    # get osc data
    with osc.data_lock:
        x = osc.gyroscope_data["x"]
        y = osc.gyroscope_data["y"]
        z = osc.gyroscope_data["z"]

    gh.draw_background()
    gh.update_ball()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.iconify()
            if event.key == pygame.K_c:
                gh.reset_club()
            if event.key == pygame.K_r:
                gh = initialize.game_initialization()
                start_time = pygame.time.get_ticks() 
    
    if not gh.is_game_finished() and not gh.is_ball_moving():
        strike_occured, direction_to_ball = gh.check_strike()

        if(strike_occured):
            gh.handle_strike(direction_to_ball)

    gh.draw_ball()
    gh.update_club_position(x, z)
    gh.draw_club()
    gh.draw_obstacles()
    gh.draw_hole()  

    if not gh.is_game_finished():
        gh.update_camera()

    if gh.check_ball_golf():
       gh.show_gameover_and_wait(start_time)
       gh = initialize.game_initialization()
       start_time = pygame.time.get_ticks() 
    else:
        gh.screen_blit_time(start_time)

    pygame.display.flip()  
    gh.get_clock().tick(60)
