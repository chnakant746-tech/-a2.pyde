import random

grid_s = [10, 10]
scr_size = [500, 500] 
hud_h = 60
colors_n = 4
start_moves = 25
target_score = 1000

swap_delay = 12
clear_delay = 15
fall_delay = 5

g = []
selected = []

score = 0
moves = 0
combo = 0
message = ""
state = "idle"           # idle / swap / clear / fall / over
wait = 0
swap_a = [0, 0]
swap_b = [0, 0]


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


def makes_match(matrix, row, col, value):
    if col >= 2:
        if matrix[row][col - 1] == value and matrix[row][col - 2] == value:
            return True

    if row >= 2:
        if matrix[row - 1][col] == value and matrix[row - 2][col] == value:
            return True

    return False


def fillin(matrix):
    row = 0

    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if matrix[row][col] == 0:
                value = random.randint(1, colors_n)

                while makes_match(matrix, row, col, value):
                    value = random.randint(1, colors_n)

                matrix[row][col] = value

            col = col + 1

        row = row + 1


def make_board():
    get_candy(g, grid_s)
    fillin(g)

    while not has_possible_move(g):
        get_candy(g, grid_s)
        fillin(g)


def new_game():
    global score, moves, combo, message, state, wait

    make_board()
    selected[:] = []
    score = 0
    moves = start_moves
    combo = 0
    message = ""
    state = "idle"
    wait = 0


def visual(matrix):
    cell_w = scr_size[0] / float(grid_s[0])
    cell_h = scr_size[1] / float(grid_s[1])

    row = 0

    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            value = matrix[row][col]

            if value != 0:
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
                    row * cell_h + cell_h / 2 + hud_h,
                    cell_w * 0.8,
                    cell_h * 0.8
                )

            col = col + 1

        row = row + 1


def draw_grid():
    cell_w = scr_size[0] / float(grid_s[0])
    cell_h = scr_size[1] / float(grid_s[1])

    stroke(0)
    strokeWeight(1)

    col = 0
    while col <= grid_s[0]:
        x = col * cell_w
        line(x, hud_h, x, hud_h + scr_size[1])
        col = col + 1

    row = 0
    while row <= grid_s[1]:
        y = hud_h + row * cell_h
        line(0, y, scr_size[0], y)
        row = row + 1


def fill_box(x, y, w, h):
    strokeCap(SQUARE)
    strokeWeight(h)
    line(x, y + h / 2.0, x + w, y + h / 2.0)
    strokeWeight(1)
    strokeCap(ROUND)


def draw_selected():
    if len(selected) == 1:
        cell_w = scr_size[0] / float(grid_s[0])
        cell_h = scr_size[1] / float(grid_s[1])

        x0 = selected[0][1] * cell_w
        y0 = hud_h + selected[0][0] * cell_h
        x1 = x0 + cell_w
        y1 = y0 + cell_h

        stroke(0)
        strokeWeight(4)
        line(x0, y0, x1, y0)
        line(x1, y0, x1, y1)
        line(x1, y1, x0, y1)
        line(x0, y1, x0, y0)
        strokeWeight(1)


def draw_hud():
    stroke(30)
    fill(30)
    fill_box(0, 0, scr_size[0], hud_h)
    noStroke()

    fill(255)
    textSize(18)
    textAlign(LEFT, CENTER)
    text("Score: " + str(score) + " / " + str(target_score), 10, 20)
    text("Moves: " + str(moves), 10, 42)

    textAlign(RIGHT, CENTER)
    text(message, scr_size[0] - 10, 30)

    if state == "over":
        stroke(0, 0, 0, 170)
        fill_box(0, hud_h, scr_size[0], scr_size[1])
        noStroke()

        fill(255)
        textAlign(CENTER, CENTER)
        textSize(36)

        if score >= target_score:
            text("YOU WIN!", scr_size[0] / 2, hud_h + scr_size[1] / 2 - 30)
        else:
            text("GAME OVER", scr_size[0] / 2, hud_h + scr_size[1] / 2 - 30)

        textSize(20)
        text("Score: " + str(score), scr_size[0] / 2, hud_h + scr_size[1] / 2 + 10)
        text("Press R to restart", scr_size[0] / 2, hud_h + scr_size[1] / 2 + 40)


def mark_matches(matrix):
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

    return remove


def has_match(matrix):
    remove = mark_matches(matrix)

    row = 0
    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if remove[row][col]:
                return True

            col = col + 1

        row = row + 1

    return False


def find_matches(matrix):
    remove = mark_matches(matrix)
    count = 0

    row = 0
    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if remove[row][col]:
                matrix[row][col] = 0
                count = count + 1

            col = col + 1

        row = row + 1

    return count


def try_swap_match(matrix, r1, c1, r2, c2):
    temp = matrix[r1][c1]
    matrix[r1][c1] = matrix[r2][c2]
    matrix[r2][c2] = temp

    result = has_match(matrix)

    temp = matrix[r1][c1]
    matrix[r1][c1] = matrix[r2][c2]
    matrix[r2][c2] = temp

    return result


def has_possible_move(matrix):
    row = 0
    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            if col + 1 < grid_s[0]:
                if try_swap_match(matrix, row, col, row, col + 1):
                    return True

            if row + 1 < grid_s[1]:
                if try_swap_match(matrix, row, col, row + 1, col):
                    return True

            col = col + 1

        row = row + 1

    return False


def drop_step(matrix):
    moved = False

    col = 0
    while col < grid_s[0]:
        row = grid_s[1] - 2

        while row >= 0:
            if matrix[row][col] != 0 and matrix[row + 1][col] == 0:
                matrix[row + 1][col] = matrix[row][col]
                matrix[row][col] = 0
                moved = True

            row = row - 1

        if matrix[0][col] == 0:
            matrix[0][col] = random.randint(1, colors_n)
            moved = True

        col = col + 1

    return moved


def swap_candy(first, second):
    y1 = first[0]
    x1 = first[1]

    y2 = second[0]
    x2 = second[1]

    if abs(y1 - y2) + abs(x1 - x2) == 1:
        temp = g[y1][x1]
        g[y1][x1] = g[y2][x2]
        g[y2][x2] = temp
        return True

    return False


def do_swap(first, second):
    global state, wait, swap_a, swap_b, message

    if swap_candy(first, second):
        swap_a = [first[0], first[1]]
        swap_b = [second[0], second[1]]
        selected[:] = []
        message = ""
        state = "swap"
        wait = swap_delay


def click_cell(row, col):
    if len(selected) == 0:
        selected.append([row, col])
        return

    first = selected[0]

    if first[0] == row and first[1] == col:
        selected[:] = []
    elif abs(first[0] - row) + abs(first[1] - col) == 1:
        do_swap(first, [row, col])
    else:
        selected[:] = [[row, col]]


def finish_turn():
    global state, message

    if score >= target_score:
        state = "over"
    elif moves <= 0:
        state = "over"
    elif not has_possible_move(g):
        make_board()
        message = "No moves - reshuffled!"
        state = "idle"
    else:
        state = "idle"


def update_game():
    global state, wait, score, moves, combo, message

    if wait > 0:
        wait = wait - 1
        return

    if state == "swap":
        if has_match(g):
            moves = moves - 1
            combo = 0
            state = "clear"
        else:
            swap_candy(swap_a, swap_b)
            message = "No match!"
            state = "idle"

    elif state == "clear":
        count = find_matches(g)

        if count > 0:
            combo = combo + 1
            score = score + count * 10 * combo

            if combo > 1:
                message = "Combo x" + str(combo) + "!"

            state = "fall"
            wait = clear_delay
        else:
            finish_turn()

    elif state == "fall":
        if drop_step(g):
            wait = fall_delay
        else:
            state = "clear"


def save_board(filename):
    file = open(filename, "w")

    row = 0

    while row < grid_s[1]:
        line_text = ""
        col = 0

        while col < grid_s[0]:
            value = g[row][col]

            if value == 1:
                line_text = line_text + "R"
            elif value == 2:
                line_text = line_text + "G"
            elif value == 3:
                line_text = line_text + "B"
            elif value == 4:
                line_text = line_text + "Y"
            else:
                line_text = line_text + "0"

            col = col + 1

        file.write(line_text + "\n")
        row = row + 1

    file.close()


def is_board_row(token):
    if len(token) != grid_s[0]:
        return False

    i = 0
    while i < len(token):
        if token[i] not in "RGBY0":
            return False

        i = i + 1

    return True


def load_board(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    rows = []

    i = 0
    while i < len(lines):
        parts = lines[i].split()

        j = 0
        while j < len(parts):
            token = parts[j].upper()

            if is_board_row(token):
                rows.append(token)

            j = j + 1

        i = i + 1

    if len(rows) < grid_s[1]:
        return False

    row = 0

    while row < grid_s[1]:
        col = 0

        while col < grid_s[0]:
            ch = rows[row][col]

            if ch == "R":
                g[row][col] = 1
            elif ch == "G":
                g[row][col] = 2
            elif ch == "B":
                g[row][col] = 3
            elif ch == "Y":
                g[row][col] = 4
            else:
                g[row][col] = 0

            col = col + 1

        row = row + 1

    return True


def mousePressed():
    if state != "idle":
        return

    if mouseY < hud_h:
        return

    cell_w = scr_size[0] / float(grid_s[0])
    cell_h = scr_size[1] / float(grid_s[1])

    col = int(mouseX / cell_w)
    row = int((mouseY - hud_h) / cell_h)

    if row >= 0 and row < grid_s[1] and col >= 0 and col < grid_s[0]:
        click_cell(row, col)


def keyPressed():
    global state, wait, combo, message

    if key == "r" or key == "R":
        new_game()

    elif key == "s" or key == "S":
        if state == "idle":
            save_board("save.txt")
            message = "Saved!"

    elif key == "l" or key == "L":
        if state == "idle":
            try:
                if load_board("save.txt"):
                    selected[:] = []
                    combo = 0
                    message = "Loaded!"
                    state = "fall" 
                    wait = 0
            except Exception:
                message = "Load failed"


def setup():
    size(scr_size[0], scr_size[1] + hud_h)
    new_game()


def draw():
    background(245)

    update_game()

    visual(g)
    draw_grid()
    draw_selected()
    draw_hud()
