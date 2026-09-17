from typing import List, Tuple, Optional, Callable
from .grid import MazeGrid, Direction, Wall
from .floodfill import FloodFillSolver


class VirtualRobot:
    """
    Autonomous Micromouse robot controller.
    Maintains physical pose, queries distance sensors (front, left, right),
    and executes movement primitives.
    """

    def __init__(self, grid: MazeGrid, start_pos: Tuple[int, int] = (0, 0), start_dir: Direction = Direction.NORTH):
        self.grid = grid
        self.x, self.y = start_pos
        self.direction = start_dir
        self.solver = FloodFillSolver(grid)

        self.steps_taken = 0
        self.turns_taken = 0
        self.visited_history: List[Tuple[int, int]] = [(self.x, self.y)]

        self.grid.mark_visited(self.x, self.y)

    def sense_and_update(self, wall_front: bool, wall_left: bool, wall_right: bool):
        """
        Translates relative sensor readings into absolute cardinal walls and updates potential field.
        """
        front_dir = self.direction
        left_dir = self.direction.turn_left
        right_dir = self.direction.turn_right

        new_walls = [
            (front_dir, wall_front),
            (left_dir, wall_left),
            (right_dir, wall_right),
        ]
        self.solver.update_walls_and_recalculate(self.x, self.y, new_walls)

    def step(self, sense_func: Callable[[int, int, Direction], Tuple[bool, bool, bool]]) -> bool:
        """
        Executes one autonomous exploration cycle:
        1. Sense walls
        2. Update potentials
        3. Determine best move
        4. Turn & Move forward
        Returns True if target reached.
        """
        # 1. Sense environment
        w_front, w_left, w_right = sense_func(self.x, self.y, self.direction)
        self.sense_and_update(w_front, w_left, w_right)

        if self.grid.is_target(self.x, self.y):
            return True

        # 2. Decide move
        best_dir = self.solver.get_best_next_move(self.x, self.y, self.direction)
        if best_dir is None:
            return False  # Trapped / unreachable

        # 3. Rotate to target heading
        if best_dir != self.direction:
            self.turns_taken += 1
            self.direction = best_dir

        # 4. Advance forward
        nx = self.x + self.direction.dx
        ny = self.y + self.direction.dy

        if self.grid.is_valid_cell(nx, ny) and not self.grid.has_wall(self.x, self.y, self.direction):
            self.x = nx
            self.y = ny
            self.steps_taken += 1
            self.visited_history.append((self.x, self.y))
            self.grid.mark_visited(self.x, self.y)

        return self.grid.is_target(self.x, self.y)
