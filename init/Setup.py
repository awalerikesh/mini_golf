""" @dataclass is a class that is designed to only hold data values """
import pygame
import random
from dataclasses import dataclass, field
from typing import Tuple, List


# Initialize pygame early
pygame.init()

# ---------------------- CONFIG DATA CLASSES ----------------------

@dataclass(frozen=True)
class ScreenSetup:
    width: int = 800
    height: int = 600
    world_width: int = 5000

    def create_screen(self) -> pygame.Surface:
        return pygame.display.set_mode((self.width, self.height))

@dataclass(frozen=True)
class FontSetup:
    text_setup = pygame.font.SysFont(None, 36)

@dataclass(frozen=True)
class Colors:
    white: Tuple[int, int, int] = (255, 255, 255)
    green: Tuple[int, int, int] = (34, 139, 34)
    red: Tuple[int, int, int] = (255, 0, 0)
    blue: Tuple[int, int, int] = (0, 0, 255)
    black: Tuple[int, int, int] = (0, 0, 0)
    brown: Tuple[int, int, int] = (139, 69, 19)
    dark_gray: Tuple[int, int, int] = (105, 105, 105)
    sky_color: Tuple[int, int, int] = (135, 206, 235)
    barrier_color: Tuple[int, int, int] = (200, 0, 0)
    purple: Tuple[int, int, int] = (128, 0, 128)


@dataclass(frozen=True)
class GolfClubSetup:
    width: int
    height: int
    distance: int
    swing_power: int
    color: Tuple[int, int, int]
    initial_position: pygame.Vector2


@dataclass(frozen=True)
class GolfBallSetup:
    screen_width: int
    screen_height: int
    initial_position: pygame.Vector2
    initial_velocity: pygame.Vector2
    radius: int
    friction: float
    min_speed: float
    color_white: Tuple[int, int, int]


@dataclass(frozen=True)
class GolfHoleSetup:
    width: int
    height: int
    hole_radius: int
    hole_position: pygame.Vector2
    outline_thickness: int
    screen_offset: pygame.Vector2
    color_black: Tuple[int, int, int]
    color_white: Tuple[int, int, int]


@dataclass
class ObstacleBarrier:
    rect: pygame.Rect
    direction: str
    speed: float


@dataclass(frozen=True)
class Whirlpool:
    center: pygame.Vector2
    radius: int


@dataclass(frozen=True)
class ObstaclesSetup:
    height: int
    width: int
    barriers: List[ObstacleBarrier]
    whirlpools: List[Whirlpool]
    circle_position: pygame.Vector2
    circle_radius: int
    circle_direction: int
    barrier_color: Tuple[int, int, int]
    whirlpool_color: Tuple[int, int, int]


@dataclass(frozen=True)
class BackgroundSetup:
    width: int
    height: int
    sky_color: Tuple[int, int, int]
    hill_color: Tuple[int, int, int]

# ------------------ Config Functions ----------------------------------------------

def create_golf_club_setup(screen: ScreenSetup, colors: Colors) -> GolfClubSetup:
    return GolfClubSetup(
        width=10,
        height=50,
        distance=30,
        swing_power=10,
        color=colors.brown,
        initial_position=pygame.Vector2(screen.width // 4, screen.height // 2)
    )

def create_golf_ball_setup(screen: ScreenSetup, colors: Colors) -> GolfBallSetup:
    return GolfBallSetup(
        screen_width=screen.width,
        screen_height=screen.height,
        initial_position=pygame.Vector2(screen.width // 4, screen.height // 2),
        initial_velocity=pygame.Vector2(0, 0),
        radius=10,
        friction=0.98,
        min_speed=0.1,
        color_white = colors.white
    )

def create_golf_hole_setup(screen: ScreenSetup, colors: Colors) -> GolfHoleSetup:
    return GolfHoleSetup(
        width = screen.width,
        height = screen.height,
        hole_radius=15,
        hole_position=pygame.Vector2(3800, screen.height // 2),
        outline_thickness=5,
        screen_offset=pygame.Vector2(1000, 0),
        color_black=colors.black,
        color_white=colors.white
    )

def create_obstacles_setup(screen: ScreenSetup, colors: Colors) -> ObstaclesSetup:
    h = screen.height
    barriers = [
        ObstacleBarrier(
            rect=pygame.Rect(x, y, 15, height),
            direction=random.choice(["up", "down"]),
            speed=1
        )
        for x, y, height in [
            (600, 200, h // 2),
            (1200, 100, h // 2),
            (1800, 100, h // 3),
            (2400, 200, h // 2),
            (3200, 100, h // 2),
            (3800, 150, h // 2),
            (4400, 150, h // 2)
        ]
    ]

    whirlpools = [
        Whirlpool(center=pygame.Vector2(x, h * y), radius=40)
        for x in [1500, 3000]
        for y in [1 / 8, 1 / 2, 7 / 8]
    ]

    return ObstaclesSetup(
        height=screen.height,
        width=screen.width,
        barriers=barriers,
        whirlpools=whirlpools,
        circle_position=pygame.Vector2(2000, 150),
        circle_radius=25,
        circle_direction=1,
        barrier_color=colors.barrier_color,
        whirlpool_color=colors.purple
    )

def create_background_setup(screen: ScreenSetup, colors: Colors) -> BackgroundSetup:
    return BackgroundSetup(
        width=screen.width,
        height=screen.height,
        sky_color=colors.sky_color,
        hill_color=colors.green
    )