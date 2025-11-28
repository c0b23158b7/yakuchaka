"""
ボード生成関連
"""
import random
from .constants import ITEM, HEAL, TRAP, RTRAP, DTRAP, WALL


def MakeBoard(size, trap, heal):
    board = [[0 for x in range(size)] for y in range(size)]

    wall_pos = [16, 18, 30, 32]
    for b in range(4):
        w_index = wall_pos[b]
        if board[w_index // size][w_index % size] == 0:
            board[w_index // size][w_index % size] = WALL

    for a in range(trap):
        while True:
            t_index = random.randrange(size * size)
            if board[t_index // size][t_index % size] == 0:
                board[t_index // size][t_index % size] = TRAP
                break
    
    for c in range(heal):
        while True:
            h_index = random.randrange(size * size)
            if board[h_index // size][h_index % size] == 0:
                board[h_index // size][h_index % size] = HEAL
                break
    
    return board


def MakeReverseBoard(size, trap, wall):
    reverse_board = [[0 for x in range(size)] for y in range(size)]
    reverse_board[3][3] = WALL

    reverse_board[3][1] = DTRAP
    danger = random.sample([[2, 0], [4, 0], [2, 1], [4, 1]], 2)
    for pos in danger:
        reverse_board[pos[0]][pos[1]] = DTRAP

    while True:
        regen = False
        w_candidates = []
        for a in range(wall):
            while True:
                w_index = random.randrange(size * size)
                if w_index not in w_candidates and w_index != 21 and w_index != 27:
                    w_candidates.append(w_index)
                    break
        for pos in w_candidates:
            c_num = 0
            for i in range(9):
                y_dif = (i // 3 - 1) * 7
                x_dif = (i % 3 - 1)
                if pos + y_dif + x_dif in w_candidates:
                    c_num += 1
                    if c_num >= 3:
                        regen = True
                        break
            if regen:
                break
        if not regen:
            break
    for spot in w_candidates:
        reverse_board[spot // size][spot % size] = WALL

    candidates = []
    for j in range(9):
        x = 3 + (j % 3) - 1
        y = 3 + (j // 3) - 1
        if reverse_board[y][x] == 0:
            candidates.append([y, x])
    if len(candidates) > 5:
        candidates = random.sample(candidates, 5)
    for pos in candidates:
        reverse_board[pos[0]][pos[1]] = RTRAP

    for b in range(trap):
        while True:
            t_index = random.randrange(size * size)
            if reverse_board[t_index // size][t_index % size] == 0 and t_index != 21 and t_index != 27:
                reverse_board[t_index // size][t_index % size] = RTRAP
                break

    return reverse_board


def MaskBoard(size, item, board):
    mask = [[0 for x in range(size)] for y in range(size)]
    for a in range(item):
        while True:
            index = random.randrange(size * size)
            if mask[index // size][index % size] == 0 and board[index // size][index % size] != WALL:
                mask[index // size][index % size] = ITEM
                break
    
    return mask


def ReverseMaskBoard(size):
    mask = [[0 for x in range(size)] for y in range(size)]
    return mask


def NoWayBoard(board, enemys):
    noway = [[0 for a in range(len(board))] for b in range(len(board))]
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == WALL:
                noway[y][x] = WALL
    for en in enemys:
        noway[en.y][en.x] = WALL
    
    return noway