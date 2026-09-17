import pytest
from tars_mazenav.core.grid import MazeGrid, Direction
from tars_mazenav.core.path_optimizer import PathOptimizer, ActionType
from tars_mazenav.simulator.maze_generator import MazeGenerator


def test_shortest_path_a_star():
    # In an open 4x4 grid with target at (3, 3)
    grid = MazeGrid(4, 4, targets=[(3, 3)])
    optimizer = PathOptimizer(grid)

    path = optimizer.find_shortest_path_a_star(start=(0, 0), start_dir=Direction.NORTH, goals=[(3, 3)])

    assert path is not None
    assert path[0][:2] == (0, 0)
    assert path[-1][:2] == (3, 3)


def test_command_compression():
    grid = MazeGrid(8, 8, targets=[(0, 3)])
    optimizer = PathOptimizer(grid)

    # 3 forward steps north: (0,0)->(0,1)->(0,2)->(0,3)
    straight_path = [
        (0, 0, Direction.NORTH),
        (0, 1, Direction.NORTH),
        (0, 2, Direction.NORTH),
        (0, 3, Direction.NORTH),
    ]

    commands = optimizer.generate_speed_run_commands(straight_path)

    # Should be compressed into single FORWARD(3)
    assert len(commands) == 1
    assert commands[0].action == ActionType.FORWARD
    assert commands[0].distance_units == 3


def test_turn_and_forward_compression():
    grid = MazeGrid(8, 8)
    optimizer = PathOptimizer(grid)

    # Move North 2, Turn East, Move East 2
    path = [
        (0, 0, Direction.NORTH),
        (0, 1, Direction.NORTH),
        (0, 2, Direction.NORTH),
        (1, 2, Direction.EAST),
        (2, 2, Direction.EAST),
    ]

    commands = optimizer.generate_speed_run_commands(path)

    assert len(commands) == 3
    assert commands[0].action == ActionType.FORWARD
    assert commands[0].distance_units == 2
    assert commands[1].action == ActionType.TURN_RIGHT
    assert commands[2].action == ActionType.FORWARD
    assert commands[2].distance_units == 2
