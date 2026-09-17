# 🏁 TARS-MazeNav: Autonomous Micromouse & Maze Solving Engine

[![CI](https://github.com/pruthvi828/tars-maze-navigation/actions/workflows/ci.yml/badge.svg)](https://github.com/pruthvi828/tars-maze-navigation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Target: ESP32 / STM32](https://img.shields.io/badge/Hardware-ESP32%20%7C%20STM32-red.svg)](#embedded-firmware)

> High-performance algorithmic engine for autonomous maze exploration, dynamic flood-fill potential fields, and high-speed trajectory compression.
> Engineered by **Team TARS** (Pruthvi Jadhav, Parth Vaishampayan, Aditi Patwa) for national robotics challenges including **IIT Bombay Techfest (MeshMerize)**, **IIT Madras Shaastra (Maze Runner)**, and **IIT Kharagpur Kshitij**.

---

## 🎯 Key Architectural Features

- **⚡ Modified Flood-Fill (Exploration Run)**:
  - Dynamic Manhattan potential field recalculation upon encountering unknown walls.
  - Directional momentum bias: prioritizes straight-line movement to eliminate unnecessary turns and motor deceleration.
  - Zero-loop guarantee across standard 16x16, 32x32, or arbitrary non-square mazes.
- **🏎️ Speed-Run Trajectory Optimization (Scoring Run)**:
  - Global graph extraction via A* with turn-cost penalties.
  - **Trapezoidal Command Compression**: Combines consecutive linear steps into continuous acceleration bursts (`FORWARD(1) + FORWARD(1) + FORWARD(1)` ➔ `FORWARD(3)`).
- **📟 Embedded C++ Firmware (`cpp_firmware/`)**:
  - Zero-heap-allocation C++ engine with circular static memory buffer (<2KB RAM).
  - Ready to flash to **ESP32-S3, ESP32-WROOM, or STM32 Nucleo** microcontrollers.
- **🎮 Micromouse Simulator (MMS) Interop**:
  - Full bidirectional I/O protocol bridge for [`mackorone/mms`](https://github.com/mackorone/mms).
- **🖥️ Terminal ASCII Visualizer**:
  - Real-time ASCII map rendering displaying walls, robot pose, and live potential fields.

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
│ - Motor Profile Compression   │
└───────────────────────────────┘
      │
      ▼
┌───────────────────────────────┐
│ Phase 3: High-Speed Run       │
│ - Smooth Trapezoidal Speed    │
│ - Max Velocity Scoring Run    │
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
pytest tests/ -v
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
