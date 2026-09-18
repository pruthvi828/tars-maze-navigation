import unittest
from tars_mazenav.core.grid import MazeGrid
from tars_mazenav.core.diagonal_optimizer import DiagonalTrajectoryOptimizer, MoveType


class TestDiagonalOptimizer(unittest.TestCase):
    def setUp(self):
        self.grid = MazeGrid(16, 16)

    def test_straight_line_compression(self):
        # Path: (0,0) -> (0,1) -> (0,2) -> (0,3)
        path = [(0, 0), (0, 1), (0, 2), (0, 3)]
        commands = DiagonalTrajectoryOptimizer.extract_diagonal_path(path, self.grid)
        
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].move_type, MoveType.FORWARD)
        self.assertEqual(commands[0].parameter, 3.0)

    def test_diagonal_stair_step_extraction(self):
        # Alternating path: (0,0) -> (0,1) -> (1,1) -> (1,2) -> (2,2)
        # Should detect diagonal stair steps and convert to 45-deg turn + DIAGONAL_FORWARD
        path = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
        commands = DiagonalTrajectoryOptimizer.extract_diagonal_path(path, self.grid)
        
        types = [cmd.move_type for cmd in commands]
        self.assertIn(MoveType.DIAGONAL_FORWARD, types)

    def test_kinematic_time_calculation(self):
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        commands = DiagonalTrajectoryOptimizer.extract_diagonal_path(path, self.grid)
        metrics = DiagonalTrajectoryOptimizer.compute_kinematic_time(commands)
        
        self.assertGreater(metrics["total_time_seconds"], 0.0)
        self.assertGreater(metrics["total_distance_meters"], 0.0)
        self.assertGreater(metrics["command_count"], 0)


if __name__ == "__main__":
    unittest.main()
