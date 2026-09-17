import pytest
from tars_mazenav.core.grid import MazeGrid, Direction
from tars_mazenav.core.floodfill import FloodFillSolver
from tars_mazenav.core.robot import VirtualRobot
from tars_mazenav.simulator.maze_generator import MazeGenerator


def test_grid_initial_potentials():
    grid = MazeGrid(16, 16)
    solver = FloodFillSolver(grid)

    # In 16x16, center cells (7,7), (7,8), (8,7), (8,8) have potential 0
    assert grid.distances[7][7] == 0
    assert grid.distances[8][8] == 0

    # Start cell (0, 0) Manhattan distance should be 7 + 7 = 14
    assert grid.distances[0][0] == 14


def test_wall_setting_bidirectional():
    grid = MazeGrid(16, 16)
    # Set wall between (0,0) and (0,1)
    grid.set_wall(0, 0, Direction.NORTH, True)

    assert grid.has_wall(0, 0, Direction.NORTH) is True
    assert grid.has_wall(0, 1, Direction.SOUTH) is True


def test_robot_exploration_convergence():
    # Generate structured maze
    ground_truth = MazeGenerator.generate_random_maze(16, 16, seed=123)
    oracle = MazeGenerator.create_sensor_oracle(ground_truth)

    robot_grid = MazeGrid(16, 16)
    robot = VirtualRobot(robot_grid, start_pos=(0, 0), start_dir=Direction.NORTH)

    reached = False
    max_steps = 500

    for _ in range(max_steps):
        if robot.step(oracle):
            reached = True
            break

    assert reached is True
    assert robot.grid.is_target(robot.x, robot.y) is True
    assert robot.steps_taken > 0
