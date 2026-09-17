import sys
from typing import Tuple
from ..core.grid import MazeGrid, Direction


class MMSAdapter:
    """
    Protocol adapter for mackorone/mms (Micromouse Simulator).
    Communicates with the simulation engine via standard input/output.
    """

    @staticmethod
    def log(message: str):
        sys.stderr.write(f"[TARS-MMS] {message}\n")
        sys.stderr.flush()

    @staticmethod
    def _command(cmd: str) -> str:
        sys.stdout.write(f"{cmd}\n")
        sys.stdout.flush()
        response = sys.stdin.readline().strip()
        return response

    @classmethod
    def get_maze_dimensions(cls) -> Tuple[int, int]:
        w = int(cls._command("mazeWidth"))
        h = int(cls._command("mazeHeight"))
        return w, h

    @classmethod
    def wall_front(cls) -> bool:
        return cls._command("wallFront") == "true"

    @classmethod
    def wall_right(cls) -> bool:
        return cls._command("wallRight") == "true"

    @classmethod
    def wall_left(cls) -> bool:
        return cls._command("wallLeft") == "true"

    @classmethod
    def move_forward(cls) -> bool:
        res = cls._command("moveForward")
        return res != "crash"

    @classmethod
    def turn_right(cls):
        cls._command("turnRight")

    @classmethod
    def turn_left(cls):
        cls._command("turnLeft")

    @classmethod
    def set_wall(cls, x: int, y: int, direction_char: str):
        cls._command(f"setWall {x} {y} {direction_char}")

    @classmethod
    def set_text(cls, x: int, y: int, text: str):
        cls._command(f"setText {x} {y} {text}")

    @classmethod
    def set_color(cls, x: int, y: int, color_char: str):
        cls._command(f"setColor {x} {y} {color_char}")
