"""
TARS-MazeNav: Autonomous Micromouse and Grid Navigation Engine
Designed for high-speed maze solving, flood-fill potential field exploration,
and trajectory optimization for IIT Techfest MeshMerize & Shaastra Maze Runner.
"""

__version__ = "1.0.0"
__author__ = "Pruthvi Jadhav (Team TARS)"

from .core.grid import MazeGrid, Direction, Wall
from .core.floodfill import FloodFillSolver
from .core.path_optimizer import PathOptimizer, MotionCommand
from .core.robot import VirtualRobot

__all__ = [
    "MazeGrid",
    "Direction",
    "Wall",
    "FloodFillSolver",
    "PathOptimizer",
    "MotionCommand",
    "VirtualRobot",
]
