# 🏁 TARS-MazeNav: Autonomous Micromouse & Robotics Simulation Studio

[![Live Interactive Demo](https://img.shields.io/badge/Live%20Demo-Interactive%20Studio-38bdf8?style=for-the-badge&logo=googlechrome&logoColor=white)](https://pruthvi828.github.io/tars-maze-navigation/)
[![CI](https://github.com/pruthvi828/tars-maze-navigation/actions/workflows/ci.yml/badge.svg)](https://github.com/pruthvi828/tars-maze-navigation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Target: ESP32 / STM32](https://img.shields.io/badge/Hardware-ESP32%20%7C%20STM32-red.svg)](#embedded-firmware)

> High-performance algorithmic engine and interactive simulation studio for autonomous maze exploration, dynamic potential fields, and 45-degree diagonal trajectory compression.
> Engineered by **Team TARS** (Pruthvi Jadhav, Parth Vaishampayan, Aditi Patwa) for national robotics championships including **IIT Bombay Techfest (MeshMerize)**, **IIT Madras Shaastra (Maze Runner)**, and **Flipkart GRiD Robotics**.

---

## 🌐 Live Interactive Studio

Try the simulation directly in your browser without installation:  
👉 **[Launch TARS-MazeNav Web Studio](https://pruthvi828.github.io/tars-maze-navigation/)**

* 🎮 **60 FPS Real-Time Canvas Simulation**: Visualizes Micromouse sensor raycasting, dynamic potential heatmaps, and wall discovery.
* ⚡ **Algorithm Comparison**: Compare Modified FloodFill vs Classical FloodFill vs A* vs 45° Diagonal Speedrun.
* 📟 **One-Click C++ Header Exporter**: Generates flash-ready C++ `#include` headers with optimal waypoints for ESP32/STM32 microcontrollers.

---

## 🎯 Key Architectural Features

- **⚡ Modified Flood-Fill (Exploration Run)**:
  - Dynamic Manhattan potential field recalculation upon encountering unknown walls.
  - Directional momentum bias: prioritizes straight-line movement to eliminate unnecessary turns and motor deceleration.
  - Zero-loop guarantee across standard 16x16, 32x32, or arbitrary non-square mazes.
- **🏎️ 45° Diagonal Trajectory Optimization (Championship Speed Run)**:
  - Converts orthogonal stair-step paths (`NORTH -> EAST -> NORTH -> EAST`) into continuous 45-degree diagonal bursts (`DIAGONAL_FORWARD(dist)`).
  - Continuous curvature kinematic modeling with trapezoidal velocity profiling ($v_{\text{max}} = 3.5\text{ m/s}, a = 12.0\text{ m/s}^2$).
- **📟 Embedded C++ Firmware (`cpp_firmware/`)**:
  - Zero-heap-allocation C++ engine with circular static memory buffer (<2KB RAM).
  - Ready to flash to **ESP32-S3, ESP32-WROOM, or STM32 Nucleo** microcontrollers.
- **🎮 Micromouse Simulator (MMS) Interop**:
  - Full bidirectional I/O protocol bridge for [`mackorone/mms`](https://github.com/mackorone/mms).

---

## 📊 Empirical Benchmark Results (25 Randomized Mazes)

| Algorithm / Phase | Avg Steps / Path | Avg Turns | Avg Scoring Time | RAM Usage |
| :--- | :---: | :---: | :---: | :---: |
| **Exploration (Modified FloodFill)** | 651.2 steps | 617.8 turns | N/A (Exploration) | **< 1.2 KB** |
| **A* Optimal Shortest Path** | 43.4 cells | 15.2 turns | 6.91 s | **< 1.8 KB** |
| **🏎️ Championship 45° Diagonal Run** | **43.4 cells** | **Smooth Curvature** | **6.86 s** | **< 1.8 KB** |

Run benchmarks locally:
```bash
python benchmark_runner.py
```

---

## 📐 Algorithm Workflow

```
[Start (0, 0)]
      │
      ▼
┌───────────────────────────────┐
│ Phase 1: Exploration Run      │◄────────┐
│ - Read ToF / IR Sensors       │         │
│ - Discover Walls              │         │
│ - Flood-Fill Recalculate      │         │
│ - Move to Lowest Potential    │─────────┘ (Loop until center reached)
└───────────────────────────────┘
      │
      ▼ (Goal Reached)
┌───────────────────────────────┐
│ Phase 2: Graph Extraction     │
│ - Generate Discovered Grid    │
│ - A* Shortest Path            │
│ - 45° Diagonal Compression    │
└───────────────────────────────┘
      │
      ▼
┌───────────────────────────────┐
│ Phase 3: Championship Run     │
│ - Trapezoidal Acceleration    │
│ - High-Speed Scoring Run      │
└───────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/pruthvi828/tars-maze-navigation.git
cd tars-maze-navigation
pip install -e .
```

### 2. Run Interactive Live Demo
```bash
python run_demo.py
```

### 3. Run Automated Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🔌 Embedded Microcontroller Pinout (ESP32)

| Component | Pin | Function |
|---|:---:|---|
| **Motor Left PWM** | `GPIO 18` | Left wheel speed modulation |
| **Motor Left DIR** | `GPIO 19` | Left H-bridge direction |
| **Motor Right PWM** | `GPIO 21` | Right wheel speed modulation |
| **Motor Right DIR** | `GPIO 22` | Right H-bridge direction |
| **Front ToF Sensor** | `GPIO 34` | Distance to front wall face |
| **Left ToF Sensor** | `GPIO 35` | Distance to left wall face |
| **Right ToF Sensor** | `GPIO 32` | Distance to right wall face |

Flash `cpp_firmware/main_esp32_demo.ino` directly using Arduino IDE or PlatformIO.

---

## 🏆 Target Competitions
- **Techfest (IIT Bombay)**: *MeshMerize* — Autonomous Maze Solving
- **Shaastra (IIT Madras)**: *Maze Runner & Line Tracer*
- **Kshitij (IIT Kharagpur)**: *Embetronix & Laws of Motion*
- **Flipkart GRiD**: *Robotics & Autonomous Mobile Robots (AMR)*

---

## 📜 License
Distributed under the **MIT License**. Created with pride by [Pruthvi Jadhav](https://github.com/pruthvi828) & Team TARS.
