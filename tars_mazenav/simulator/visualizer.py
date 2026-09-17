from ..core.grid import MazeGrid, Direction, Wall


class TerminalVisualizer:
    """
    ASCII & ANSI color terminal renderer for maze solving and potential field visualization.
    """

    HEADING_ICONS = {
        Direction.NORTH: "^",
        Direction.EAST:  ">",
        Direction.SOUTH: "v",
        Direction.WEST:  "<",
    }

    @classmethod
    def render_grid(cls, grid: MazeGrid, robot_x: int = -1, robot_y: int = -1, robot_dir: Direction = Direction.NORTH, show_potentials: bool = False) -> str:
        lines = []

        # Render from top row (y = height - 1) down to 0
        for y in range(grid.height - 1, -1, -1):
            # 1. Top wall line of row y
            top_line = ""
            for x in range(grid.width):
                top_line += "+"
                if grid.has_wall(x, y, Direction.NORTH):
                    top_line += "---"
                else:
                    top_line += "   "
            top_line += "+"
            lines.append(top_line)

            # 2. Cell content and vertical walls
            cell_line = ""
            for x in range(grid.width):
                if grid.has_wall(x, y, Direction.WEST):
                    cell_line += "|"
                else:
                    cell_line += " "

                # Content inside cell
                if x == robot_x and y == robot_y:
                    icon = cls.HEADING_ICONS.get(robot_dir, "R")
                    cell_line += f" {icon} "
                elif grid.is_target(x, y):
                    cell_line += " * "
                elif show_potentials:
                    dist = grid.distances[x][y]
                    cell_line += f"{dist:3d}" if dist < 100 else " . "
                elif grid.visited[x][y]:
                    cell_line += " . "
                else:
                    cell_line += "   "

            # Rightmost border of the row
            if grid.has_wall(grid.width - 1, y, Direction.EAST):
                cell_line += "|"
            else:
                cell_line += " "
            lines.append(cell_line)

        # 3. Bottom wall of row 0
        bottom_line = ""
        for x in range(grid.width):
            bottom_line += "+"
            if grid.has_wall(x, 0, Direction.SOUTH):
                bottom_line += "---"
            else:
                bottom_line += "   "
        bottom_line += "+"
        lines.append(bottom_line)

        return "\n".join(lines)
