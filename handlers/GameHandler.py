import components as gc
import pygame
import sys

class GameHandler:
    def __init__(self, background: gc.Background, screen, ball: gc.GolfBall, club: gc.GolfClub, hole: gc.GolfHole, obstacles: gc.Obstacles, height, width, world_width):
        self._background: gc.Background = background
        self._screen = screen
        self._ball: gc.GolfBall = ball
        self._club: gc.GolfClub = club
        self._hole: gc.GolfHole = hole
        self._obstacles: gc.Obstacles = obstacles
        self._screen_width = width
        self._screen_height = height
        self._world_width = world_width
        self._camera_x = 0
        self._clock = pygame.time.Clock()
        self._game_finished = False
        self._running = True
        self._update_club = False

    
    def set_camera_x(self, camera_x):
        self._camera_x = camera_x

    def set_game_status(self, status):
        self._game_finished = status

    def set_update_club(self, status):
        self._update_club = status
    
    def set_running_game(self, status):
        self._running = status

    def get_running_game(self):
        return self._running

    def get_update_club(self):
        return self._update_club
    
    def get_camera_x(self):
        return self._camera_x
    
    def get_screen(self):
        return self._screen
    
    def get_screen_width(self):
        return self._screen_width
    
    def get_screen_height(self):
        return self._screen_height
    
    def get_clock(self):
        return self._clock

    def is_game_finished(self):
        return self._game_finished
    
    """Check if the club strikes the ball"""
    def check_strike(self):

        prev_club_position = self._ball.get_ball_position() - pygame.Vector2(20, 0)
        self._club.set_previous_club_position(prev_club_position)

        screen_ball_position = self._ball.get_ball_position() + pygame.Vector2(self._ball.get_ball_radius() * 2, 0) - pygame.Vector2(self._camera_x, 0)

        # Vector from club to ball
        direction_to_ball = screen_ball_position - self._club.get_current_club_position()
        distance_to_ball = direction_to_ball.length()

        # Check if the club is close enough and approaching from the left
        is_close_enough = distance_to_ball <= self._ball.get_ball_radius() + self._club.get_width() // 2
        is_from_left = self._club.get_current_club_position().x <= screen_ball_position.x

        if is_close_enough and is_from_left:
            return True, direction_to_ball

        return False, direction_to_ball 
    
    """Calculate the ball velocity using the previous and current ball position"""
    def calculate_ball_velocity(self, direction_to_ball):
        speed = (self._club.get_current_club_position() - self._club.get_previous_club_position()).length()
        strike_power = min(speed, self._club.get_swing_power())
        direction = direction_to_ball.normalize()
        ball_velocity = (direction * strike_power) * 1.4
        self._ball.set_ball_velocity(ball_velocity)
    
    """Updates the ball's position and handles friction, boundaries, and collisions."""
    def update_ball(self):
        if self._ball.get_ball_velocity().length() > 0.1:
            self._apply_friction()   # Apply friction to the ball
            ball_position = self._ball.get_ball_position()
            ball_velocity = self._ball.get_ball_velocity()
            ball_position += ball_velocity # Move the ball
            self._ball.set_ball_position(ball_position)
            self._ball.draw(self._screen, self.get_camera_x())   # Draw the updated ball position
        else:
            self._stop_ball() # If ball velocity is too small, stop the ball

        self._apply_whirlpool_force()
        # Check and handle boundary collisions (edges of the screen)
        self._check_and_handle_boundaries()

        # Check and handle collisions with barriers (obstacles)
        self._handle_barrier_collision()

    def update_camera(self):
        camera_x = max(0, min(self._ball.get_ball_position().x - self.get_screen_width() // 4, 5000 - self.get_screen_width()))
        self.set_camera_x(camera_x)

    def is_ball_moving(self):
        return self._ball.is_moving()
    
    """Applies friction to the ball's velocity and stops the ball if the speed is below the minimum."""
    def _apply_friction(self):
        ball_velocity = self._ball.get_ball_velocity()
        ball_velocity *= self._ball.get_ball_friction()
        self._ball.set_ball_velocity(ball_velocity)
        if self._ball.get_ball_velocity().length() < self._ball.get_ball_min_speed():
            self._ball.set_ball_velocity(pygame.Vector2(0, 0)) 

    """Stops the ball by setting its velocity to zero."""
    def _stop_ball(self):
        self._ball.set_ball_velocity(pygame.Vector2(0, 0))

    def handle_strike(self, direction_to_ball):
        self.set_update_club(True)
        self.calculate_ball_velocity(direction_to_ball)
        self.update_ball()
    
    def update_club_position(self, x, z):
        if self._ball.is_moving():
            club_position = self._club.update_club_position(x, z, self.get_screen_height(), self.get_screen_width())
        elif(self.get_update_club() and not self._ball.is_moving()):
            club_position = self._ball.get_ball_position() - pygame.Vector2(20, 0) - pygame.Vector2(self._camera_x, 0)
            self._club.set_current_club_position(club_position)
            self.set_update_club(False)
        else:
            self._club.update_club_position(x, z, self.get_screen_height(), self.get_screen_width())


    """Checks for collisions with obstacles (barriers) and adjusts the ball's velocity upon impact."""
    def _handle_barrier_collision(self):
        for barrier in self._obstacles.get_barriers():
            ball_rect = pygame.Rect(self._ball.get_ball_position().x - self._ball.get_ball_radius(), self._ball.get_ball_position().y - self._ball.get_ball_radius(), self._ball.get_ball_radius() * 2, self._ball.get_ball_radius() * 2)
            if barrier.rect.colliderect(ball_rect):
                self.play_rebound_sound()
                ball_velocity = self._ball.get_ball_velocity()
                if barrier.rect.width > barrier.rect.height:
                    ball_velocity.y *= -1
                else:
                    ball_velocity.x *= -1
                self._ball.set_ball_velocity(ball_velocity)
    
    """Checks and handles boundary collisions (edges of the screen)."""
    def _check_and_handle_boundaries(self):
        self._check_horizontal_boundaries()
        self._check_vertical_boundaries()

    """Checks if the ball has hit the horizontal boundaries (left or right)."""
    def _check_horizontal_boundaries(self):
        ball_velocity = self._ball.get_ball_velocity()
        ball_position = self._ball.get_ball_position()
        ball_radius = self._ball.get_ball_radius()
        if ball_position.x - ball_radius < 0 or ball_position.x + ball_radius > self._world_width:
            self.play_rebound_sound()
            ball_velocity.x *= -1
            ball_position.x = max(ball_radius, min(ball_position.x, self._world_width - ball_radius))
        self._ball.set_ball_position(ball_position)
        self._ball.set_ball_velocity(ball_velocity)


    """Checks if the ball has hit the vertical boundaries (top or bottom)."""
    def _check_vertical_boundaries(self):
        ball_velocity = self._ball.get_ball_velocity()
        ball_position = self._ball.get_ball_position()
        ball_radius = self._ball.get_ball_radius()
        screen_height = self._ball.get_screen_height()
        if ball_position.y - ball_radius < 0 or ball_position.y + ball_radius > screen_height:
            self.play_rebound_sound()
            ball_velocity.y *= -1
            ball_position.y = max(ball_radius, min(ball_position.y, screen_height - ball_radius))
        self._ball.set_ball_position(ball_position)
        self._ball.set_ball_velocity(ball_velocity)

    def check_ball_golf(self):
        ball_pos = self._ball.get_ball_position() + pygame.Vector2(self._ball.get_ball_radius() * 2, 0) - pygame.Vector2(self._camera_x, 0)
        hole_pos = self._hole.get_hole_position() - pygame.Vector2(self._camera_x, 0) + self._hole._screen_offset
        if abs(ball_pos.x - hole_pos.x) < 10 and abs(ball_pos.y - hole_pos.y) < 10:
            self.set_running_game(False)
            self.update_ball()
            self._ball.set_ball_velocity(pygame.Vector2(0, 0))
            return True

    def show_image_and_wait(self):
        image = pygame.image.load(r".\img\startscreen.PNG")
        screen = self.get_screen()
        screen_height = self.get_screen_height()
        screen_width = self.get_screen_width()
        image = pygame.transform.scale(image, (screen_height, screen_width))
        screen.blit(image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return False
        return True
                    
    def _apply_whirlpool_force(self):
        ball_velocity = self._ball.get_ball_velocity()
        ball_pos = self._ball.get_ball_position()
        for wp in self._obstacles.get_whirlpools():
            dist = (ball_pos - wp.center).length()
            if dist < wp.radius:
                direction = (wp.center - ball_pos).normalize()
                perpendicular = pygame.Vector2(-direction.y, direction.x)
                ball_velocity += direction * 0.8 + perpendicular * 0.8
        self._ball.set_ball_velocity(ball_velocity)

    def reset_club(self):
        club_position = self._ball.get_ball_position() - pygame.Vector2(20, 0) - pygame.Vector2(self._camera_x, 0)
        self._club.set_current_club_position(club_position)
        self.set_update_club(True)

    def reset_game(self):
        self.set_camera_x(0)

    def play_strike_sound(self):
        pygame.mixer.init()
        hit_sound = pygame.mixer.Sound(r".\sound\golf-ball-hit.wav")  
        hit_sound.set_volume(0.5)  
        pygame.mixer.Sound.play(hit_sound)  
            
    def play_rebound_sound(self):
        pygame.mixer.init()
        rebound_sound = pygame.mixer.Sound(r".\sound\rebound.wav")  
        rebound_sound.set_volume(0.5)  
        pygame.mixer.Sound.play(rebound_sound) 

    def draw_ball(self):
        self._ball.draw(self.get_screen(), self.get_camera_x())

    def draw_club(self):
        self._club.draw_golf_stick(self.get_screen())

    def draw_background(self):
        self._background.draw_background(self.get_camera_x())

    def draw_obstacles(self):
        self._obstacles.draw(self.get_camera_x())

    def draw_hole(self):
        self._hole.draw_hole(self.get_camera_x())  