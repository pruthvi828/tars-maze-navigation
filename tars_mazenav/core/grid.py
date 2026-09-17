from enum import IntEnum, auto
from typing import List, Tuple, Set, Optional


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def dx(self) -> int:
        return [0, 1, 0, -1][self.value]

    @property
    def dy(self) -> int:
        return [1, 0, -1, 0][self.value]

    @property
    def opposite(self) -> "Direction":
        return Direction((self.value + 2) % 4)

    @property
    def turn_right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

    @property
    def turn_left(self) -> "Direction":
        return Direction((self.value + 3) % 4)


class Wall:
    NORTH = 1 << 0  # 1
    EAST  = 1 << 1  # 2
    SOUTH = 1 << 2  # 4
    WEST  = 1 << 3  # 8

    DIR_TO_WALL = {
        Direction.NORTH: NORTH,
        Direction.EAST:  EAST,
        Direction.SOUTH: SOUTH,
        Direction.WEST:  WEST,
    }


class MazeGrid:
    """
    Representation of a Micromouse maze grid.
    Supports arbitrary sizes (default 16x16 standard competition).
    Tracks discovered walls, Manhattan potential distances, and visited cells.
    """

    def __init__(self, width: int = 16, height: int = 16, targets: Optional[List[Tuple[int, int]]] = None):
        self.width = width
        self.height = height

        # Initialize walls: only outer boundaries are known initially
        self.walls = [[0 for _ in range(height)] for _ in range(width)]
        self.distances = [[255 for _ in range(height)] for _ in range(width)]
        self.visited = [[False for _ in range(height)] for _ in range(width)]

        # Default standard 4 center cells for 16x16 Micromouse
        if targets is None:
            if width == 16 and height == 16:
                self.targets = [(7, 7), (7, 8), (8, 7), (8, 8)]
            else:
                self.targets = [(width // 2, height // 2)]
        else:
            self.targets = targets

        self._init_outer_boundaries()

    def _init_outer_boundaries(self):
        """Add permanent outer perimeter walls of the maze arena."""
        for x in range(self.width):
            self.walls[x][0] |= Wall.SOUTH
            self.walls[x][self.height - 1] |= Wall.NORTH

        for y in range(self.height):
            self.walls[0][y] |= Wall.WEST
            self.walls[self.width - 1][y] |= Wall.EAST

    def is_valid_cell(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        if not self.is_valid_cell(x, y):
            return True
        flag = Wall.DIR_TO_WALL[direction]
        return bool(self.walls[x][y] & flag)

    def set_wall(self, x: int, y: int, direction: Direction, present: bool = True):
        """Set a wall bidirectionally between cell (x, y) and its neighbor."""
        if not self.is_valid_cell(x, y):
            return

        flag = Wall.DIR_TO_WALL[direction]
        if present:
            self.walls[x][y] |= flag
        else:
            self.walls[x][y] &= ~flag

        # Update adjacent neighbor cell
        nx = x + direction.dx
        ny = y + direction.dy
        if self.is_valid_cell(nx, ny):
            opp_flag = Wall.DIR_TO_WALL[direction.opposite]
            if present:
                self.walls[nx][ny] |= opp_flag
            else:
                self.walls[nx][ny] &= ~opp_flag

    def get_accessible_neighbors(self, x: int, y: int) -> List[Tuple[int, int, Direction]]:
        """Returns reachable neighbors without walls."""
        neighbors = []
        for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
            if not self.has_wall(x, y, direction):
                nx = x + direction.dx
                ny = y + direction.dy
                if self.is_valid_cell(nx, ny):
                    neighbors.append((nx, ny, direction))
        return neighbors

    def mark_visited(self, x: int, y: int):
        if self.is_valid_cell(x, y):
            self.visited[x][y] = True

    def is_target(self, x: int, y: int) -> bool:
        return (x, y) in self.targets
