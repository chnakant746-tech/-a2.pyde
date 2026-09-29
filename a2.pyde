import random

grid_s = [10, 10]
scr_size = [500, 500]

g = []

def get_candy(grid, grid_size):
    i = 0
    while i < grid_size[0]:
        grid.append([])
        i = i + 1

def fillin(grid_x, grid_y, matrix):
    y = 0
    while y < grid_y:
        x = 0
        while x < grid_x:
            matrix[y].append(random.randint(1, 4))
            x = x + 1
        y = y + 1

def setup():
    size(scr_size[0], scr_size[1])
    get_candy(g, grid_s)
    fillin(grid_s[0], grid_s[1], g)

def visual(grid_x, grid_y, scr_sizex, scr_sizey, matrix):
    cell_w = scr_sizex / grid_x
    cell_h = scr_sizey / grid_y
    y = 0
    while y < grid_y:
        x = 0
        while x < grid_x:
            val = matrix[y][x]
            if val == 1:
                fill(255, 80, 80)    # R
            elif val == 2:
                fill(80, 255, 80)    # G
            elif val == 3:
                fill(80, 80, 255)    # B
            elif val == 4:
                fill(255, 255, 80)   # Y
            else:
                fill(220)
            ellipse(x * cell_w + cell_w/2, y * cell_h + cell_h/2, cell_w * 0.8, cell_h * 0.8)
            x = x + 1
        y = y + 1

def three_del(grid_x, grid_y, matrix):
    y = 0
    while y < grid_y:
        x = 0
        while x < grid_x - 2:
            if matrix[y][x] != 0 and matrix[y][x] == matrix[y][x+1] == matrix[y][x+2]:
                matrix[y][x] = 0
                matrix[y][x+1] = 0
                matrix[y][x+2] = 0
            x = x + 1
        y = y + 1

    y = 0
    while y < grid_y - 2:
        x = 0
        while x < grid_x:
            if matrix[y][x] != 0 and matrix[y+1][x] == matrix[y+2][x] == matrix[y][x]:
                matrix[y][x] = 0
                matrix[y+1][x] = 0
                matrix[y+2][x] = 0
            x = x + 1
        y = y + 1

def fall(grid_x, grid_y, matrix):
    x = 0
    while x < grid_x:
        y = grid_y - 1
        while y > 0:
            if matrix[y][x] == 0:
                matrix[y][x] = matrix[y-1][x]
                matrix[y-1][x] = random.randint(1, 4)
            y = y - 1
        x = x + 1

def mousePressed():
    pass

def draw():
    background(255)
    three_del(grid_s[0], grid_s[1], g)
    fall(grid_s[0], grid_s[1], g)
    visual(grid_s[0], grid_s[1], scr_size[0], scr_size[1], g)
