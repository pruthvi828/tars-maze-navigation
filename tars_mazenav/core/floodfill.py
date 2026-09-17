from collections import deque
from typing import List, Tuple, Optional
from .grid import MazeGrid, Direction


class FloodFillSolver:
    """
    High-Performance Modified Flood-Fill Algorithm.
    Computes optimal distance potentials and selects moves with directional inertia
    to minimize unnecessary turns and motor deceleration.
    """

    def __init__(self, grid: MazeGrid):
        self.grid = grid
        self.reset_potentials()

    def reset_potentials(self, custom_targets: Optional[List[Tuple[int, int]]] = None):
        """
        Initializes distance field using breadth-first propagation from targets.
        """
        targets = custom_targets or self.grid.targets
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.grid.distances[x][y] = 255

        queue = deque()
        for tx, ty in targets:
            self.grid.distances[tx][ty] = 0
            queue.append((tx, ty))

        # BFS initial Manhattan distance field assuming zero walls
        while queue:
            cx, cy = queue.popleft()
            curr_dist = self.grid.distances[cx][cy]

            for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
                nx, ny = cx + d.dx, cy + d.dy
                if self.grid.is_valid_cell(nx, ny):
                    if self.grid.distances[nx][ny] == 255:
                        self.grid.distances[nx][ny] = curr_dist + 1
                        queue.append((nx, ny))

    def update_walls_and_recalculate(self, current_x: int, current_y: int, new_walls: List[Tuple[Direction, bool]]):
        """
        Updates discovered walls and triggers queue-based potential field update if needed.
        """
        wall_changed = False
        for direction, present in new_walls:
            if self.grid.has_wall(current_x, current_y, direction) != present:
                self.grid.set_wall(current_x, current_y, direction, present)
                wall_changed = True

        if wall_changed:
            self.recompute_potentials(current_x, current_y)

    def recompute_potentials(self, start_x: int, start_y: int):
        """
        Standard Micromouse Queue-based Flood Fill recalculation.
        Guarantees strictly descending path to target cells.
        """
        queue = deque([(start_x, start_y)])

        while queue:
            cx, cy = queue.popleft()

            # Target cells always maintain potential 0
            if self.grid.is_target(cx, cy):
                continue

            accessible = self.grid.get_accessible_neighbors(cx, cy)
            if not accessible:
                continue

            min_neighbor_dist = min(self.grid.distances[nx][ny] for nx, ny, _ in accessible)

            # If current cell does not equal 1 + min(neighbors), update and cascade
            if self.grid.distances[cx][cy] != min_neighbor_dist + 1:
                self.grid.distances[cx][cy] = min_neighbor_dist + 1

                # Push current cell and all its accessible neighbors
                for nx, ny, _ in accessible:
                    queue.append((nx, ny))

    def get_best_next_move(self, x: int, y: int, current_direction: Direction) -> Optional[Direction]:
        """
        Selects next move with lowest potential.
        Tie-breaking: prefers continuing straight in current heading to avoid turns.
        """
        accessible = self.grid.get_accessible_neighbors(x, y)
        if not accessible:
            return None

        # Find minimum distance among accessible neighbors
        min_dist = min(self.grid.distances[nx][ny] for nx, ny, _ in accessible)
        candidates = [d for nx, ny, d in accessible if self.grid.distances[nx][ny] == min_dist]

        # Prioritize maintaining straight momentum if available
        if current_direction in candidates:
            return current_direction

        # Secondary: right turn, then left turn, avoid 180 u-turn if possible
        if current_direction.turn_right in candidates:
            return current_direction.turn_right
        if current_direction.turn_left in candidates:
            return current_direction.turn_left

        return candidates[0]
