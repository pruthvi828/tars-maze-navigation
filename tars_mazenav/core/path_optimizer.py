from enum import Enum, auto
from typing import List, Tuple, Optional
from dataclasses import dataclass
import heapq
from .grid import MazeGrid, Direction


class ActionType(Enum):
    FORWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    TURN_AROUND = auto()
    DIAGONAL_LEFT = auto()
    DIAGONAL_RIGHT = auto()


@dataclass
class MotionCommand:
    action: ActionType
    distance_units: int = 1  # For FORWARD: number of cell lengths
    description: str = ""

    def __str__(self):
        if self.action == ActionType.FORWARD:
            return f"FORWARD({self.distance_units} cells)"
        return f"{self.action.name}"


class PathOptimizer:
    """
    Computes global shortest path on discovered maze graph
    and optimizes step sequence into smooth high-speed motor profiles.
    """

    def __init__(self, grid: MazeGrid):
        self.grid = grid

    def find_shortest_path_a_star(
        self,
        start: Tuple[int, int] = (0, 0),
        start_dir: Direction = Direction.NORTH,
        goals: Optional[List[Tuple[int, int]]] = None
    ) -> Optional[List[Tuple[int, int, Direction]]]:
        """
        A* search on discovered walls, penalizing turns to encourage straight runs.
        State: (cost, x, y, direction)
        """
        goals = goals or self.grid.targets
        goal_set = set(goals)

        # Priority Queue: (f_score, g_score, x, y, direction, path)
        open_set = []
        heapq.heappush(open_set, (0, 0, start[0], start[1], start_dir, [(start[0], start[1], start_dir)]))

        visited_states = {}

        while open_set:
            f, g, x, y, d, path = heapq.heappop(open_set)

            if (x, y) in goal_set:
                return path

            state_key = (x, y, d)
            if state_key in visited_states and visited_states[state_key] <= g:
                continue
            visited_states[state_key] = g

            # Evaluate neighbors
            for nx, ny, nd in self.grid.get_accessible_neighbors(x, y):
                # Calculate turn penalty
                turn_cost = 0
                if nd != d:
                    if nd == d.turn_right or nd == d.turn_left:
                        turn_cost = 2.0  # 90-degree turn penalty
                    else:
                        turn_cost = 4.0  # 180-degree U-turn penalty

                step_cost = 1.0 + turn_cost
                new_g = g + step_cost

                # Heuristic: minimum Manhattan distance to any goal
                h = min(abs(nx - gx) + abs(ny - gy) for gx, gy in goals)
                new_f = new_g + h

                new_path = path + [(nx, ny, nd)]
                heapq.heappush(open_set, (new_f, new_g, nx, ny, nd, new_path))

        return None

    def generate_speed_run_commands(self, path: List[Tuple[int, int, Direction]]) -> List[MotionCommand]:
        """
        Compresses step-by-step path into trapezoidal acceleration commands.
        Collapses consecutive forwards: [F, F, F] -> FORWARD(3)
        """
        if not path or len(path) < 2:
            return []

        raw_actions: List[ActionType] = []
        curr_dir = path[0][2]

        for i in range(len(path) - 1):
            next_dir = path[i + 1][2]

            # Turning required
            if next_dir != curr_dir:
                if next_dir == curr_dir.turn_right:
                    raw_actions.append(ActionType.TURN_RIGHT)
                elif next_dir == curr_dir.turn_left:
                    raw_actions.append(ActionType.TURN_LEFT)
                elif next_dir == curr_dir.opposite:
                    raw_actions.append(ActionType.TURN_AROUND)
                curr_dir = next_dir

            raw_actions.append(ActionType.FORWARD)

        # Compress linear forwards
        compressed_commands: List[MotionCommand] = []
        forward_run = 0

        for action in raw_actions:
            if action == ActionType.FORWARD:
                forward_run += 1
            else:
                if forward_run > 0:
                    compressed_commands.append(MotionCommand(ActionType.FORWARD, forward_run))
                    forward_run = 0
                compressed_commands.append(MotionCommand(action, 1))

        if forward_run > 0:
            compressed_commands.append(MotionCommand(ActionType.FORWARD, forward_run))

        return compressed_commands
