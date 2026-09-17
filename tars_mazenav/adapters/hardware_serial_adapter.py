import time
from typing import Tuple, Optional


class HardwareSerialAdapter:
    """
    UART Communication bridge for physical ESP32 / STM32 robot chassis.
    Formats motion primitives and parses raw Time-of-Flight / IR sensor telemetry.
    """

    def __init__(self, port: str = "COM3", baudrate: int = 115200, wall_threshold_cm: float = 12.0):
        self.port = port
        self.baudrate = baudrate
        self.wall_threshold_cm = wall_threshold_cm
        self.serial_conn = None

    def connect(self) -> bool:
        try:
            import serial
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1.0)
            time.sleep(1.5)  # ESP32 boot delay
            return True
        except Exception:
            return False  # Fallback to simulation mode if hardware is unplugged

    def read_sensors(self) -> Tuple[bool, bool, bool]:
        """
        Queries micro-controller sensors and returns (wall_front, wall_left, wall_right).
        Expected hardware response: "TELEM:<dist_f>,<dist_l>,<dist_r>\n"
        """
        if not self.serial_conn:
            return (False, False, False)

        try:
            self.serial_conn.write(b"PING_SENSORS\n")
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line.startswith("TELEM:"):
                parts = line.replace("TELEM:", "").split(",")
                df, dl, dr = float(parts[0]), float(parts[1]), float(parts[2])
                return (
                    df < self.wall_threshold_cm,
                    dl < self.wall_threshold_cm,
                    dr < self.wall_threshold_cm
                )
        except Exception:
            pass
        return (False, False, False)

    def send_motion(self, command_str: str) -> bool:
        """Sends motion primitive to motor controller."""
        if not self.serial_conn:
            return False
        try:
            self.serial_conn.write(f"{command_str}\n".encode('utf-8'))
            return True
        except Exception:
            return False
