import random

grid_s = [10, 10]
scr_size = [500, 500]

g = []
selected = []


def get_candy(grid, size):
    grid[:] = []
    row = 0

    while row < size[1]:
        new_row = []
        col = 0

        while col < size[0]:
            new_row.append(0)
            col = col + 1

        grid.append(new_row)
        row = row + 1


def fillin(matrix):
    row = 0

    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if matrix[row][col] == 0:
                matrix[row][col] = random.randint(1, 4)

            col = col + 1

        row = row + 1


def visual(matrix):
    cell_w = scr_size[0] / grid_s[0]
    cell_h = scr_size[1] / grid_s[1]

    row = 0

    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            value = matrix[row][col]

            if value == 1:
                fill(255, 80, 80)
            elif value == 2:
                fill(80, 255, 80)
            elif value == 3:
                fill(80, 80, 255)
            elif value == 4:
                fill(255, 220, 80)

            noStroke()

            ellipse(
                col * cell_w + cell_w / 2,
                row * cell_h + cell_h / 2,
                cell_w * 0.8,
                cell_h * 0.8
            )

            col = col + 1

        row = row + 1


def draw_grid():
    cell_w = scr_size[0] / grid_s[0]
    cell_h = scr_size[1] / grid_s[1]

    stroke(0)
    strokeWeight(1)

    col = 0
    while col <= grid_s[0]:
        x = col * cell_w
        line(x, 0, x, scr_size[1])
        col = col + 1

    row = 0
    while row <= grid_s[1]:
        y = row * cell_h
        line(0, y, scr_size[0], y)
        row = row + 1


def find_matches(matrix):
    remove = []

    row = 0
    while row < grid_s[1]:
        temp = []
        col = 0

        while col < grid_s[0]:
            temp.append(False)
            col = col + 1

        remove.append(temp)
        row = row + 1

    row = 0
    while row < grid_s[1]:
        col = 0

        while col < grid_s[0] - 2:
            value = matrix[row][col]

            if value != 0:
                if value == matrix[row][col + 1] and value == matrix[row][col + 2]:
                    remove[row][col] = True
                    remove[row][col + 1] = True
                    remove[row][col + 2] = True

            col = col + 1

        row = row + 1

    col = 0
    while col < grid_s[0]:
        row = 0

        while row < grid_s[1] - 2:
            value = matrix[row][col]

            if value != 0:
                if value == matrix[row + 1][col] and value == matrix[row + 2][col]:
                    remove[row][col] = True
                    remove[row + 1][col] = True
                    remove[row + 2][col] = True

            row = row + 1

        col = col + 1

    row = 0
    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if remove[row][col]:
                matrix[row][col] = 0

            col = col + 1

        row = row + 1


def fall_candies(matrix):
    col = 0

    while col < grid_s[0]:
        row = grid_s[1] - 1

        while row >= 0:
            if matrix[row][col] == 0:
                above = row - 1

                while above >= 0 and matrix[above][col] == 0:
                    above = above - 1

                if above >= 0:
                    matrix[row][col] = matrix[above][col]
                    matrix[above][col] = 0
                else:
                    matrix[row][col] = random.randint(1, 4)

            row = row - 1

        col = col + 1


def save_board(filename):
    file = open(filename, "w")

    row = 0

    while row < grid_s[1]:
        text = ""
        col = 0

        while col < grid_s[0]:
            value = g[row][col]

            if value == 1:
                text = text + "R"
            elif value == 2:
                text = text + "G"
            elif value == 3:
                text = text + "B"
            elif value == 4:
                text = text + "Y"
            else:
                text = text + "0"

            col = col + 1

        file.write(text + "\n")
        row = row + 1

    file.close()


def load_board(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    row = 0

    while row < grid_s[1] and row < len(lines):
        line = lines[row].strip()
        col = 0

        while col < grid_s[0] and col < len(line):
            if line[col] == "R":
                g[row][col] = 1
            elif line[col] == "G":
                g[row][col] = 2
            elif line[col] == "B":
                g[row][col] = 3
            elif line[col] == "Y":
                g[row][col] = 4
            else:
                g[row][col] = 0

            col = col + 1

        row = row + 1


def swap_candy(first, second):
    y1 = first[0]
    x1 = first[1]

    y2 = second[0]
    x2 = second[1]

    if abs(y1 - y2) + abs(x1 - x2) == 1:
        temp = g[y1][x1]
        g[y1][x1] = g[y2][x2]
        g[y2][x2] = temp


def mousePressed():
    cell_w = scr_size[0] / grid_s[0]
    cell_h = scr_size[1] / grid_s[1]

    col = int(mouseX / cell_w)
    row = int(mouseY / cell_h)

    if row >= 0 and row < grid_s[1] and col >= 0 and col < grid_s[0]:
        selected.append([row, col])

        if len(selected) == 2:
            swap_candy(selected[0], selected[1])
            selected[:] = []


def keyPressed():
    if key == "s" or key == "S":
        save_board("save.txt")

    elif key == "l" or key == "L":
        load_board("save.txt")


def setup():
    size(scr_size[0], scr_size[1])
    get_candy(g, grid_s)
    fillin(g)


def draw():
    background(245)

    find_matches(g)
    fall_candies(g)
    fillin(g)

    visual(g)
    draw_grid()
