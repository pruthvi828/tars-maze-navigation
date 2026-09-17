/**
 * TARS-MazeNav: Autonomous ESP32 Micromouse Firmware
 * Target: ESP32-WROOM-32 / ESP32-S3 / STM32 Nucleo
 * Designed for Team TARS at IIT Techfest MeshMerize & Shaastra Maze Runner
 */

#include <Arduino.h>
#include "floodfill.hpp"

// ================= Pin Configuration =================
#define PIN_MOTOR_L_PWM  18
#define PIN_MOTOR_L_DIR  19
#define PIN_MOTOR_R_PWM  21
#define PIN_MOTOR_R_DIR  22

#define PIN_SENSOR_FRONT 34 // ADC or I2C XSHUT
#define PIN_SENSOR_LEFT  35
#define PIN_SENSOR_RIGHT 32

#define WALL_THRESHOLD_MM 130 // mm to wall face

FloodFillEngine engine;

uint8_t robot_x = 0;
uint8_t robot_y = 0;
Direction robot_heading = DIR_NORTH;

enum RobotState {
    EXPLORATION_TO_CENTER,
    EXPLORATION_TO_START,
    OPTIMIZED_SPEED_RUN
};
RobotState current_state = EXPLORATION_TO_CENTER;

// Low-level motor primitives
void motorDriveForward() {
    digitalWrite(PIN_MOTOR_L_DIR, HIGH);
    digitalWrite(PIN_MOTOR_R_DIR, HIGH);
    ledcWrite(0, 180); // Speed calibration
    ledcWrite(1, 180);
    delay(280); // Wheel encoder tick duration per cell
    ledcWrite(0, 0);
    ledcWrite(1, 0);
    delay(50);
}

void motorTurnRight90() {
    digitalWrite(PIN_MOTOR_L_DIR, HIGH);
    digitalWrite(PIN_MOTOR_R_DIR, LOW);
    ledcWrite(0, 150);
    ledcWrite(1, 150);
    delay(140);
    ledcWrite(0, 0);
    ledcWrite(1, 0);
    delay(50);
}

void motorTurnLeft90() {
    digitalWrite(PIN_MOTOR_L_DIR, LOW);
    digitalWrite(PIN_MOTOR_R_DIR, HIGH);
    ledcWrite(0, 150);
    ledcWrite(1, 150);
    delay(140);
    ledcWrite(0, 0);
    ledcWrite(1, 0);
    delay(50);
}

void motorTurn180() {
    motorTurnRight90();
    delay(40);
    motorTurnRight90();
}

// Sensor reading helper
void readSensors(bool &wall_front, bool &wall_left, bool &wall_right) {
    // Read analog/ToF sensors
    int raw_f = analogRead(PIN_SENSOR_FRONT);
    int raw_l = analogRead(PIN_SENSOR_LEFT);
    int raw_r = analogRead(PIN_SENSOR_RIGHT);

    wall_front = (raw_f > 1500);
    wall_left  = (raw_l > 1500);
    wall_right = (raw_r > 1500);
}

void setup() {
    Serial.begin(115200);
    pinMode(PIN_MOTOR_L_DIR, OUTPUT);
    pinMode(PIN_MOTOR_R_DIR, OUTPUT);

    Serial.println("[TARS] Micromouse System Initialized.");
    delay(1000);
}

void loop() {
    if (engine.isTarget(robot_x, robot_y)) {
        Serial.println("[TARS] Center Goal Achieved! Exploration completed.");
        while (1) { delay(1000); }
    }

    // 1. Read sensors
    bool w_front, w_left, w_right;
    readSensors(w_front, w_left, w_right);

    // 2. Map walls into engine
    Direction left_dir  = (Direction)((robot_heading + 3) % 4);
    Direction right_dir = (Direction)((robot_heading + 1) % 4);

    engine.setWall(robot_x, robot_y, robot_heading, w_front);
    engine.setWall(robot_x, robot_y, left_dir, w_left);
    engine.setWall(robot_x, robot_y, right_dir, w_right);

    // 3. Recalculate potentials if current cell is not optimal
    engine.recalculatePotentials(robot_x, robot_y);

    // 4. Determine next heading
    Direction next_dir = engine.getBestNextMove(robot_x, robot_y, robot_heading);

    // 5. Execute turn
    if (next_dir == right_dir) {
        motorTurnRight90();
    } else if (next_dir == left_dir) {
        motorTurnLeft90();
    } else if (next_dir == (Direction)((robot_heading + 2) % 4)) {
        motorTurn180();
    }
    robot_heading = next_dir;

    // 6. Step forward
    motorDriveForward();
    robot_x += (robot_heading == DIR_EAST) ? 1 : (robot_heading == DIR_WEST ? -1 : 0);
    robot_y += (robot_heading == DIR_NORTH) ? 1 : (robot_heading == DIR_SOUTH ? -1 : 0);

    Serial.printf("Pose: (%d, %d) Heading: %d Dist: %d\n", robot_x, robot_y, robot_heading, engine.getDistance(robot_x, robot_y));
    delay(40);
}
