from dataclasses import dataclass

@dataclass
class ScreenConfig:
    width: int = 1280
    height: int = 720
    title: str = "Pygame"

@dataclass
class GameConfig:
    screen: ScreenConfig
    fps_cap: int = 60

config = GameConfig(screen=ScreenConfig())