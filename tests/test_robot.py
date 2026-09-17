import pytest
from tars_mazenav.core.grid import MazeGrid, Direction
from tars_mazenav.core.robot import VirtualRobot
from tars_mazenav.simulator.maze_generator import MazeGenerator


def test_robot_init():
    grid = MazeGrid(16, 16)
    robot = VirtualRobot(grid, start_pos=(0, 0), start_dir=Direction.NORTH)

    assert robot.x == 0
    assert robot.y == 0
    assert robot.direction == Direction.NORTH
    assert robot.steps_taken == 0
    assert robot.turns_taken == 0
    assert len(robot.visited_history) == 1
    assert grid.visited[0][0] is True


def test_robot_sense_and_update():
    grid = MazeGrid(8, 8)
    robot = VirtualRobot(grid, start_pos=(2, 2), start_dir=Direction.NORTH)

    # Robot facing North: front is North, left is West, right is East
    robot.sense_and_update(wall_front=True, wall_left=False, wall_right=True)

    assert grid.has_wall(2, 2, Direction.NORTH) is True
    assert grid.has_wall(2, 2, Direction.WEST) is False
    assert grid.has_wall(2, 2, Direction.EAST) is True
    # Check adjacent cell symmetry
    assert grid.has_wall(2, 3, Direction.SOUTH) is True
    assert grid.has_wall(3, 2, Direction.WEST) is True


def test_robot_trapped_dead_end():
    # Enclose cell (0, 0) completely
    grid = MazeGrid(4, 4, targets=[(3, 3)])
    robot = VirtualRobot(grid, start_pos=(0, 0), start_dir=Direction.NORTH)

    # Oracle returns walls on all sides
    def wall_trap_oracle(x, y, d):
        return (True, True, True)

    reached = robot.step(wall_trap_oracle)
    assert reached is False
    assert robot.steps_taken == 0
