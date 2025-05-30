import pygame
import handlers.GameHandler as game_handlers
import handlers.gyroscopeHandler as osc
import init as initialize
import sys

########################### osc thread init ###############################
osc.osc_thread_start()

###################### game component init ################################
game_handlers = initialize.game_initialization()
pygame.display.set_caption("Mini Golf")

###################### game init ###########################################
pygame.init()
clock = pygame.time.Clock()
start_screen = True

while start_screen:
    status = game_handlers.show_image_and_wait()
    if(status == False):
       start_screen = False

while True:
    # get osc data
    with osc.data_lock:
        x = osc.gyroscope_data["x"]
        y = osc.gyroscope_data["y"]
        z = osc.gyroscope_data["z"]

    game_handlers.draw_background()
    game_handlers.update_ball()
    game_handlers.draw_club()
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.iconify()
    
    if not game_handlers.is_game_finished() and not game_handlers.is_ball_moving():
        strike_occured, direction_to_ball = game_handlers.check_strike()
        if(strike_occured):
            game_handlers.play_strike_sound()

            game_handlers.handle_strike(direction_to_ball)

    game_handlers.draw_ball()
    game_handlers.update_club_position(x, z)
    game_handlers.draw_club()
    game_handlers.draw_obstacles()
    game_handlers.draw_hole()  

    if not game_handlers.is_game_finished():
        game_handlers.update_camera()

    if game_handlers.check_ball_golf():
       initialize.screen_blit_game_finished(game_handlers.get_screen())
    else:
        initialize.screen_blit_time(game_handlers.get_screen())
    pygame.display.flip()  
    game_handlers.get_clock().tick(60)
