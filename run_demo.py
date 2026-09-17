#!/usr/bin/env python3
"""
TARS-MazeNav: Autonomous Micromouse Interactive Demonstration
Simulates a live autonomous run:
1. Phase 1: Exploration & Mapping via Modified Flood-Fill
2. Phase 2: Shortest-Path Extraction & Trapezoidal Motion Compression
"""

import time
from tars_mazenav.core.grid import MazeGrid, Direction
from tars_mazenav.core.robot import VirtualRobot
from tars_mazenav.core.path_optimizer import PathOptimizer
from tars_mazenav.simulator.maze_generator import MazeGenerator
from tars_mazenav.simulator.visualizer import TerminalVisualizer


def run_full_mission():
    print("=" * 65)
    print(" 🚀 TARS-MazeNav: Autonomous Micromouse Navigation Engine")
    print(" Developed by Team TARS (IIT Techfest & Shaastra Autonomous Track)")
    print("=" * 65)

    # 1. Generate Ground-Truth Arena (8x8 for clear terminal display)
    width, height = 8, 8
    target = [(width // 2, height // 2), (width // 2 - 1, height // 2)]
    print(f"\n[1/3] Generating competition maze ({width}x{height}) with central goal...")
    ground_truth = MazeGenerator.generate_random_maze(width, height, seed=2026)
    oracle = MazeGenerator.create_sensor_oracle(ground_truth)

    # 2. Phase 1: Exploration Run
    print("\n[2/3] Starting Autonomous Exploration Run (Modified Flood-Fill)...")
    robot_grid = MazeGrid(width, height, targets=target)
    robot = VirtualRobot(robot_grid, start_pos=(0, 0), start_dir=Direction.NORTH)

    max_steps = 300
    step_count = 0

    while step_count < max_steps:
        reached = robot.step(oracle)
        step_count += 1
        if reached:
            break

    print(f"✔ Goal reached in {robot.steps_taken} steps with {robot.turns_taken} turns!")
    print("\nDiscovered Maze & Potential Distance Field:")
    print(TerminalVisualizer.render_grid(robot_grid, robot.x, robot.y, robot.direction, show_potentials=True))

    # 3. Phase 2: High-Speed Run Optimization
    print("\n[3/3] Calculating Speed-Run Trajectory (A* Graph Compression)...")
    optimizer = PathOptimizer(robot_grid)
    optimal_path = optimizer.find_shortest_path_a_star(start=(0, 0), start_dir=Direction.NORTH, goals=target)

    if optimal_path:
        print(f"✔ Optimal Path Length: {len(optimal_path)} cells")
        commands = optimizer.generate_speed_run_commands(optimal_path)

        print("\n🏁 High-Speed Motor Profile Commands:")
        for idx, cmd in enumerate(commands, 1):
            print(f"  Step {idx:02d}: {cmd}")

        print("\n" + "=" * 65)
        print(" Mission Accomplished! Ready to flash to ESP32 / STM32 hardware.")
        print("=" * 65)
    else:
        print("⚠ Path calculation failed.")


if __name__ == "__main__":
    run_full_mission()
