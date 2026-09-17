import pytest
from tars_mazenav.core.grid import MazeGrid, Direction
from tars_mazenav.simulator.maze_generator import MazeGenerator
from tars_mazenav.simulator.visualizer import TerminalVisualizer


def test_maze_generator_dimensions():
    grid = MazeGenerator.generate_random_maze(width=8, height=8, seed=42)
    assert grid.width == 8
    assert grid.height == 8
    # Outer boundaries should be present
    for x in range(8):
        assert grid.has_wall(x, 0, Direction.SOUTH) is True
        assert grid.has_wall(x, 7, Direction.NORTH) is True


def test_sensor_oracle():
    grid = MazeGrid(4, 4)
    grid.set_wall(0, 0, Direction.NORTH, True)
    grid.set_wall(0, 0, Direction.EAST, False)

    oracle = MazeGenerator.create_sensor_oracle(grid)
    # Robot at (0, 0) facing NORTH:
    # front is NORTH (wall: True), left is WEST (boundary: True), right is EAST (wall: False)
    wf, wl, wr = oracle(0, 0, Direction.NORTH)
    assert wf is True
    assert wl is True
    assert wr is False


def test_terminal_visualizer_render():
    grid = MazeGrid(4, 4, targets=[(2, 2)])
    rendered_plain = TerminalVisualizer.render_grid(grid)
    assert "+" in rendered_plain
    assert "*" in rendered_plain

    rendered_with_robot = TerminalVisualizer.render_grid(grid, robot_x=0, robot_y=0, robot_dir=Direction.NORTH)
    assert "^" in rendered_with_robot

    rendered_potentials = TerminalVisualizer.render_grid(grid, show_potentials=True)
    assert isinstance(rendered_potentials, str)
    assert len(rendered_potentials) > 0
