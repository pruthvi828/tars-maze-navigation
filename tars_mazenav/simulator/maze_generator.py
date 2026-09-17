import random
from typing import List, Tuple, Set
from ..core.grid import MazeGrid, Direction, Wall


class MazeGenerator:
    """
    Generates competition-compliant random or structured Micromouse mazes.
    Uses Randomized Depth-First Search with central goal preservation.
    """

    @classmethod
    def generate_random_maze(cls, width: int = 16, height: int = 16, seed: int = 42) -> MazeGrid:
        random.seed(seed)
        grid = MazeGrid(width, height)

        # Initially, place walls everywhere inside
        for x in range(width):
            for y in range(height):
                for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                    grid.set_wall(x, y, d, True)

        visited: Set[Tuple[int, int]] = set()
        stack: List[Tuple[int, int]] = []

        start = (0, 0)
        visited.add(start)
        stack.append(start)

        # Center goal reserve (keep open between center cells)
        center_cells = set(grid.targets)

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors = []

            for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                nx, ny = cx + d.dx, cy + d.dy
                if grid.is_valid_cell(nx, ny) and (nx, ny) not in visited:
                    unvisited_neighbors.append((nx, ny, d))

            if unvisited_neighbors:
                nx, ny, direction = random.choice(unvisited_neighbors)
                # Knock down wall between current and neighbor
                grid.set_wall(cx, cy, direction, False)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # Ensure center goal cells have inter-connections
        for cx, cy in center_cells:
            for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                nx, ny = cx + d.dx, cy + d.dy
                if (nx, ny) in center_cells:
                    grid.set_wall(cx, cy, d, False)

        return grid

    @classmethod
    def create_sensor_oracle(cls, grid: MazeGrid):
        """
        Returns a callable: (x, y, heading) -> (wall_front, wall_left, wall_right)
        simulating physical laser/IR sensors against the ground truth maze.
        """
        def oracle(x: int, y: int, heading: Direction) -> Tuple[bool, bool, bool]:
            wf = grid.has_wall(x, y, heading)
            wl = grid.has_wall(x, y, heading.turn_left)
            wr = grid.has_wall(x, y, heading.turn_right)
            return (wf, wl, wr)

        return oracle
