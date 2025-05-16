import pygame
import components as gc
import handlers as osc
import init as initialize

########################### osc thread init ###############################
osc.osc_thread_start()

###################### game component init ################################
game_objects = initialize.game_initialization()
screen = game_objects["screen"]
background: gc.Background = game_objects["background"]
club: gc.GolfClub = game_objects["club"]
obstacles: gc.Obstacles = game_objects["obstacles"]
ball: gc.GolfBall = game_objects["ball"]
hole: gc.GolfHole = game_objects["hole"]
screen_height = game_objects["screen_height"]
screen_width = game_objects["screen_width"]
world_width = game_objects["world_width"]
pygame.display.set_caption("Parallax Background Example")

###################### Initial ball and club position  #####################
screen_ball_position = ball.get_ball_position()
club_position = screen_ball_position - pygame.Vector2(20, 0)
prev_club_position = club_position.copy()

###################### game init ###########################################
pygame.init()
club_ball_offset = pygame.Vector2(20, 0)
camera_x = 0
clock = pygame.time.Clock()
game_finished = False
running = True
update_club = False

while running:

    # get osc data
    with osc.data_lock:
        x = osc.gyroscope_data["x"]
        y = osc.gyroscope_data["y"]
        z = osc.gyroscope_data["z"]

    # draw background
    background.draw_background(camera_x) 
    ball.update(screen, obstacles, camera_x)
    club.draw_golf_stick(club_position) 
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.iconify()
    
    # check if game is finished or not
    if not game_finished and not ball.is_moving():
        prev_club_position = ball.get_ball_position() - club_ball_offset

        # check for a strike
        strike_occurred, direction = club.check_strike(club_position, ball, camera_x)
        if(strike_occurred):
            update_club = True
            club.calculate_ball_velocity(prev_club_position, club_position, direction, ball)
            ball.update(screen, obstacles, camera_x) 
  
    ball.draw(screen, camera_x) 

    if ball.is_moving():
        club_position = club.update_club_position(club_position, x, z, screen_height, screen_width)
    elif(update_club and not ball.is_moving()):
        club_position = ball.get_ball_position() - club_ball_offset - pygame.Vector2(camera_x, 0)
        update_club = False
    else:
        club_position = club.update_club_position(club_position, x, z, screen_height, screen_width)
        
    club.draw_golf_stick(club_position)    
    hole.draw_hole(camera_x)
    obstacles.draw(camera_x)

    if not game_finished:
        camera_x = max(0, min(ball.get_ball_position().x - screen_width // 4, world_width - screen_width))

    initialize.screen_blit(screen)
    pygame.display.flip()  
    clock.tick(60)  

pygame.quit()
