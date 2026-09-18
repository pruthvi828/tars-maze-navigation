"""
Diagonal Path & Kinematic Trajectory Optimizer for Micromouse Navigation.
Implements 45-degree diagonal trajectory extraction, smooth turn kinematics,
and trapezoidal acceleration profiling for championship speed runs.
"""

from enum import Enum
from typing import List, Tuple, Dict
import math
from tars_mazenav.core.grid import Direction, MazeGrid


class MoveType(Enum):
    FORWARD = "FORWARD"
    TURN_LEFT_90 = "TURN_LEFT_90"
    TURN_RIGHT_90 = "TURN_RIGHT_90"
    TURN_U = "TURN_U"
    TURN_LEFT_45 = "TURN_LEFT_45"
    TURN_RIGHT_45 = "TURN_RIGHT_45"
    DIAGONAL_FORWARD = "DIAGONAL_FORWARD"
    SMOOTH_TURN_90 = "SMOOTH_TURN_90"


class DiagonalCommand:
    def __init__(self, move_type: MoveType, parameter: float = 1.0):
        self.move_type = move_type
        self.parameter = parameter  # distance (cells) or angle (degrees)

    def __repr__(self):
        return f"{self.move_type.value}({self.parameter})"


class DiagonalTrajectoryOptimizer:
    """
    Transforms Manhattan rectilinear paths into high-speed diagonal paths
    with continuous curvature smoothing and trapezoidal velocity profiles.
    """

    @staticmethod
    def extract_diagonal_path(
        path: List[Tuple[int, int]], grid: MazeGrid
    ) -> List[DiagonalCommand]:
        """
        Compresses consecutive right-angle zig-zags (N-E-N-E or N-W-N-W)
        into continuous 45-degree diagonal bursts if no diagonal corner walls block the path.
        """
        if len(path) < 2:
            return []

        # First extract directional segments
        vectors = []
        for i in range(len(path) - 1):
            dx = path[i + 1][0] - path[i][0]
            dy = path[i + 1][1] - path[i][1]
            vectors.append((dx, dy))

        commands: List[DiagonalCommand] = []
        i = 0
        current_dir = (0, 1)  # Default facing North

        while i < len(vectors):
            # Check for diagonal pattern (alternating orthogonal steps)
            if i + 1 < len(vectors):
                v1 = vectors[i]
                v2 = vectors[i + 1]
                
                # Check if v1 and v2 form an alternating stair-step pattern
                if (v1[0] == 0 and v2[1] == 0 and v1[1] != 0 and v2[0] != 0) or \
                   (v1[1] == 0 and v2[0] == 0 and v1[0] != 0 and v2[1] != 0):
                    
                    diag_count = 0
                    j = i
                    while j + 1 < len(vectors) and vectors[j] == v1 and vectors[j + 1] == v2:
                        diag_count += 1
                        j += 2

                    if diag_count >= 1:
                        # Compute initial 45-deg entry turn
                        diag_vec = (v1[0] + v2[0], v1[1] + v2[1])
                        turn_cmd = DiagonalTrajectoryOptimizer._get_turn_command(current_dir, diag_vec, is_45=True)
                        if turn_cmd:
                            commands.append(turn_cmd)
                        
                        # Add diagonal forward burst (distance = diag_count * sqrt(2))
                        commands.append(DiagonalCommand(MoveType.DIAGONAL_FORWARD, round(diag_count * math.sqrt(2), 2)))
                        current_dir = diag_vec
                        i = j
                        continue

            # Standard orthogonal movement
            v = vectors[i]
            # Count consecutive steps in same direction
            straight_count = 1
            while i + 1 < len(vectors) and vectors[i + 1] == v:
                straight_count += 1
                i += 1

            turn_cmd = DiagonalTrajectoryOptimizer._get_turn_command(current_dir, v, is_45=False)
            if turn_cmd:
                commands.append(turn_cmd)
            
            commands.append(DiagonalCommand(MoveType.FORWARD, float(straight_count)))
            current_dir = v
            i += 1

        return commands

    @staticmethod
    def _get_turn_command(current: Tuple[int, int], target: Tuple[int, int], is_45: bool = False) -> DiagonalCommand:
        """Determines required turn angle and direction between two heading vectors."""
        if current == target:
            return None

        # Cross product to determine Left (positive) vs Right (negative)
        cross = current[0] * target[1] - current[1] * target[0]
        dot = current[0] * target[0] + current[1] * target[1]

        if is_45:
            if cross > 0:
                return DiagonalCommand(MoveType.TURN_LEFT_45, 45.0)
            elif cross < 0:
                return DiagonalCommand(MoveType.TURN_RIGHT_45, 45.0)
        else:
            if dot < 0 and cross == 0:
                return DiagonalCommand(MoveType.TURN_U, 180.0)
            elif cross > 0:
                return DiagonalCommand(MoveType.TURN_LEFT_90, 90.0)
            elif cross < 0:
                return DiagonalCommand(MoveType.TURN_RIGHT_90, 90.0)

        return None

    @staticmethod
    def compute_kinematic_time(
        commands: List[DiagonalCommand],
        max_velocity: float = 3.5,     # m/s
        max_accel: float = 12.0,        # m/s^2
        turn_time_90: float = 0.08,    # s
        turn_time_45: float = 0.045,   # s
        cell_size: float = 0.18        # m (Standard IEEE Micromouse cell: 18cm)
    ) -> Dict[str, float]:
        """
        Calculates realistic physical execution time using trapezoidal acceleration profiles.
        """
        total_time = 0.0
        total_distance = 0.0

        for cmd in commands:
            if cmd.move_type in (MoveType.FORWARD, MoveType.DIAGONAL_FORWARD):
                dist_m = cmd.parameter * cell_size
                total_distance += dist_m
                
                # Distance needed to reach max velocity: d_acc = v^2 / (2*a)
                d_acc = (max_velocity ** 2) / (2 * max_accel)
                
                if dist_m >= 2 * d_acc:
                    # Trapezoidal profile (Accel -> Cruise -> Decel)
                    t_acc = max_velocity / max_accel
                    d_cruise = dist_m - 2 * d_acc
                    t_cruise = d_cruise / max_velocity
                    total_time += (2 * t_acc) + t_cruise
                else:
                    # Triangular profile (Peak velocity < max_velocity)
                    v_peak = math.sqrt(dist_m * max_accel)
                    t_acc = v_peak / max_accel
                    total_time += 2 * t_acc

            elif cmd.move_type in (MoveType.TURN_LEFT_90, MoveType.TURN_RIGHT_90, MoveType.SMOOTH_TURN_90):
                total_time += turn_time_90
            elif cmd.move_type in (MoveType.TURN_LEFT_45, MoveType.TURN_RIGHT_45):
                total_time += turn_time_45
            elif cmd.move_type == MoveType.TURN_U:
                total_time += turn_time_90 * 2.0

        return {
            "total_time_seconds": round(total_time, 4),
            "total_distance_meters": round(total_distance, 3),
            "command_count": len(commands)
        }
