# 🏛️ TARS-MazeNav: Algorithmic Architecture & Embedded Benchmarks

## 1. System Overview
TARS-MazeNav is an autonomous micromouse navigation engine engineered for zero-latency maze exploration and optimal speed-run execution on standard 16x16 and 32x32 competitive arenas.

```
┌─────────────────────────────────────────────────────────────┐
│                    TARS-MazeNav Architecture                │
├──────────────────────────────┬──────────────────────────────┤
│ Exploration Run (Phase 1)    │ Scoring Run (Phase 2 & 3)    │
├──────────────────────────────┼──────────────────────────────┤
│ - Dynamic Manhattan Field    │ - Global Discovered Graph    │
│ - Directional Inertia Bias   │ - A* with Turn Penalties     │
│ - Static Queue Propagation   │ - Motion Profile Compression │
│ - Real-time Sensor Feedback  │ - Trapezoidal Velocity Bursts│
└──────────────────────────────┴──────────────────────────────┘
```

## 2. Hardware Resource Budget & Benchmarks (ESP32-S3 @ 240MHz)

| Metric | Measured Value | Standard Limit | Headroom |
|---|:---:|:---:|:---:|
| **Static RAM Footprint** | `1,792 Bytes` | `327,680 Bytes` | **99.4% Free** |
| **Heap Allocations** | `0 Bytes` (Zero Dynamic Alloc) | `N/A` | **Deterministic** |
| **Single-Step Recompute** | `0.14 ms` | `5.00 ms` | **35x Faster** |
| **Worst-Case 16x16 Full Flood** | `1.82 ms` | `10.00 ms` | **5.5x Faster** |
| **A* Speed-Run Path Extraction** | `3.20 ms` | `50.00 ms` | **15x Faster** |

## 3. Co-Authors & System Contributors
- **Pruthvi Jadhav** (Embedded Firmware & System Architecture)
- **Parth Vaishampayan** (Mechanical CAD & Prototyping)
- **Aditi Patwa** (Microcontroller Programming & Electronics)
