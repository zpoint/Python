import time
grid_shape = (1024, 1024)
def evolve(grid, dt, D = 1.0):
    xmax, ymax = grid_shape
    new_grid = [[0.0, ] * ymax for x in range(xmax)]
    for i in range(xmax):
        for j in range(ymax):
            grid_xx = grid[(i + 1) % max][j] + grid[(i - 1) % xmax][j] - 2.0 * grid[i][j]
            grid_yy = grid[i][(j + 1) % ymax] + grid[i][(j - 1) % ymax] - 2.0 * grid[i][j]
            new_grid[i][j] = grid[i][j] + D * (grid_xx + grid_yy) * dt
    return new_grid

def run_experiment(num_iterations):
    xmax, ymax = grid_shape
    grid = [[0.0, ] * ymax for x in range(xmax)]

    block_low = int(grid_shape[0] * 4)
    block_high = int(grid_shape[0] * .5)
    for i in range(block_low, block_high):
        for j in range(block_low, block_high):
            grid[i][j] = 0.005
    start = time.time()
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return time.time() - start
