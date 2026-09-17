#include "floodfill.hpp"

const int8_t DX[4] = {0, 1, 0, -1};
const int8_t DY[4] = {1, 0, -1, 0};
const uint8_t OPPOSITE_WALL[4] = {WALL_SOUTH, WALL_WEST, WALL_NORTH, WALL_EAST};
const uint8_t DIR_WALL[4] = {WALL_NORTH, WALL_EAST, WALL_SOUTH, WALL_WEST};

FloodFillEngine::FloodFillEngine() {
    target_min_x = 7; target_max_x = 8;
    target_min_y = 7; target_max_y = 8;
    q_head = 0;
    q_tail = 0;

    // Clear walls and distances
    for (uint8_t x = 0; x < MAZE_WIDTH; ++x) {
        for (uint8_t y = 0; y < MAZE_HEIGHT; ++y) {
            walls[x][y] = 0;
            // Initial Manhattan distance estimation to center
            int dist_x = (x < 7) ? (7 - x) : (x > 8 ? x - 8 : 0);
            int dist_y = (y < 7) ? (7 - y) : (y > 8 ? y - 8 : 0);
            distances[x][y] = (uint8_t)(dist_x + dist_y);
        }
    }

    // Set boundary walls
    for (uint8_t x = 0; x < MAZE_WIDTH; ++x) {
        walls[x][0] |= WALL_SOUTH;
        walls[x][MAZE_HEIGHT - 1] |= WALL_NORTH;
    }
    for (uint8_t y = 0; y < MAZE_HEIGHT; ++y) {
        walls[0][y] |= WALL_WEST;
        walls[MAZE_WIDTH - 1][y] |= WALL_EAST;
    }
}

bool FloodFillEngine::isTarget(uint8_t x, uint8_t y) const {
    return (x >= target_min_x && x <= target_max_x &&
            y >= target_min_y && y <= target_max_y);
}

void FloodFillEngine::setWall(uint8_t x, uint8_t y, Direction dir, bool present) {
    if (x >= MAZE_WIDTH || y >= MAZE_HEIGHT) return;

    if (present) {
        walls[x][y] |= DIR_WALL[dir];
    } else {
        walls[x][y] &= ~DIR_WALL[dir];
    }

    int8_t nx = x + DX[dir];
    int8_t ny = y + DY[dir];
    if (nx >= 0 && nx < MAZE_WIDTH && ny >= 0 && ny < MAZE_HEIGHT) {
        if (present) {
            walls[nx][ny] |= OPPOSITE_WALL[dir];
        } else {
            walls[nx][ny] &= ~OPPOSITE_WALL[dir];
        }
    }
}

bool FloodFillEngine::hasWall(uint8_t x, uint8_t y, Direction dir) const {
    if (x >= MAZE_WIDTH || y >= MAZE_HEIGHT) return true;
    return (walls[x][y] & DIR_WALL[dir]) != 0;
}

void FloodFillEngine::enqueue(uint8_t x, uint8_t y) {
    queue[q_tail].x = x;
    queue[q_tail].y = y;
    q_tail = (q_tail + 1) & 0xFF; // Wrap-around at 256
}

bool FloodFillEngine::dequeue(uint8_t &x, uint8_t &y) {
    if (q_head == q_tail) return false;
    x = queue[q_head].x;
    y = queue[q_head].y;
    q_head = (q_head + 1) & 0xFF;
    return true;
}

bool FloodFillEngine::isQueueEmpty() const {
    return q_head == q_tail;
}

void FloodFillEngine::recalculatePotentials(uint8_t start_x, uint8_t start_y) {
    q_head = 0;
    q_tail = 0;
    enqueue(start_x, start_y);

    uint8_t cx, cy;
    while (dequeue(cx, cy)) {
        if (isTarget(cx, cy)) continue;

        uint8_t min_neighbor = UNREACHABLE;
        for (uint8_t d = 0; d < 4; ++d) {
            if (!hasWall(cx, cy, (Direction)d)) {
                int8_t nx = cx + DX[d];
                int8_t ny = cy + DY[d];
                if (nx >= 0 && nx < MAZE_WIDTH && ny >= 0 && ny < MAZE_HEIGHT) {
                    if (distances[nx][ny] < min_neighbor) {
                        min_neighbor = distances[nx][ny];
                    }
                }
            }
        }

        if (min_neighbor != UNREACHABLE && distances[cx][cy] != min_neighbor + 1) {
            distances[cx][cy] = min_neighbor + 1;

            // Push neighbors for update
            for (uint8_t d = 0; d < 4; ++d) {
                if (!hasWall(cx, cy, (Direction)d)) {
                    int8_t nx = cx + DX[d];
                    int8_t ny = cy + DY[d];
                    if (nx >= 0 && nx < MAZE_WIDTH && ny >= 0 && ny < MAZE_HEIGHT) {
                        enqueue(nx, ny);
                    }
                }
            }
        }
    }
}

Direction FloodFillEngine::getBestNextMove(uint8_t x, uint8_t y, Direction current_heading) {
    uint8_t min_dist = UNREACHABLE;
    Direction best_dir = current_heading;
    bool found = false;

    // Check all 4 accessible directions
    for (uint8_t d = 0; d < 4; ++d) {
        Direction dir = (Direction)d;
        if (!hasWall(x, y, dir)) {
            int8_t nx = x + DX[dir];
            int8_t ny = y + DY[dir];
            if (nx >= 0 && nx < MAZE_WIDTH && ny >= 0 && ny < MAZE_HEIGHT) {
                uint8_t dist = distances[nx][ny];
                if (dist < min_dist) {
                    min_dist = dist;
                    best_dir = dir;
                    found = true;
                } else if (dist == min_dist && dir == current_heading) {
                    // Straight-line momentum bias to avoid turning
                    best_dir = dir;
                }
            }
        }
    }

    return best_dir;
}
