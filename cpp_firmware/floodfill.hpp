#ifndef TARS_FLOODFILL_HPP
#define TARS_FLOODFILL_HPP

#include <stdint.h>

#define MAZE_WIDTH 16
#define MAZE_HEIGHT 16
#define UNREACHABLE 255

enum Direction : uint8_t {
    DIR_NORTH = 0,
    DIR_EAST = 1,
    DIR_SOUTH = 2,
    DIR_WEST = 3
};

#define WALL_NORTH (1 << 0)
#define WALL_EAST  (1 << 1)
#define WALL_SOUTH (1 << 2)
#define WALL_WEST  (1 << 3)

class FloodFillEngine {
public:
    FloodFillEngine();

    void initTargets(uint8_t t1_x, uint8_t t1_y, uint8_t t2_x, uint8_t t2_y);
    void setWall(uint8_t x, uint8_t y, Direction dir, bool present);
    bool hasWall(uint8_t x, uint8_t y, Direction dir) const;
    void recalculatePotentials(uint8_t start_x, uint8_t start_y);
    Direction getBestNextMove(uint8_t x, uint8_t y, Direction current_heading);

    uint8_t getDistance(uint8_t x, uint8_t y) const { return distances[x][y]; }
    bool isTarget(uint8_t x, uint8_t y) const;

private:
    uint8_t walls[MAZE_WIDTH][MAZE_HEIGHT];
    uint8_t distances[MAZE_WIDTH][MAZE_HEIGHT];

    uint8_t target_min_x, target_min_y;
    uint8_t target_max_x, target_max_y;

    // Static circular queue for embedded microcontrollers (zero heap allocation)
    struct CellCoord {
        uint8_t x;
        uint8_t y;
    };
    CellCoord queue[256];
    uint8_t q_head;
    uint8_t q_tail;

    void enqueue(uint8_t x, uint8_t y);
    bool dequeue(uint8_t &x, uint8_t &y);
    bool isQueueEmpty() const;
};

#endif // TARS_FLOODFILL_HPP
