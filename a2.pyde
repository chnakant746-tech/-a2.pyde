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
    pass

def three_del(grid_x, grid_y, matrix):
    pass

def fall(grid_x, grid_y, matrix):
    pass

def mousePressed():
    pass

def draw():
    background(255)
