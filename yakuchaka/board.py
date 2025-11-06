import random
from .constants import TRAP, WALL, HEAL, RTRAP, DTRAP, ITEM

def MakeBoard(size, trap, wall, heal):
    board = [[0 for x in range(size)] for y in range(size)]
    for a in range(trap):
        while(True):
            t_index = random.randrange(size*size)
            if(board[t_index // size][t_index % size] != TRAP):
                board[t_index // size][t_index % size] = TRAP
                break

    for b in range(wall):
        while(True):
            w_index = random.randrange(size*size)
            if(board[w_index // size][w_index % size] == 0):
                board[w_index // size][w_index % size] = WALL
                break
    
    for c in range(heal):
        while(True):
            h_index = random.randrange(size*size)
            if(board[h_index // size][h_index % size] == 0):
                board[h_index // size][h_index % size] = HEAL
                break
    
    return board

def MakeReverseBoard(size, trap, wall):
    reverse_board = [[0 for x in range(size)] for y in range(size)]
    reverse_board[3][3] = WALL

    reverse_board[3][1] = DTRAP
    danger = random.sample([[2,0],[4,0],[2,1],[4,1]], 2)
    for pos in danger:
        reverse_board[pos[0]][pos[1]] = DTRAP

    for a in range(wall):
        while(True):
            w_index = random.randrange(size*size)
            if(reverse_board[w_index // size][w_index % size] == 0 and w_index != 21):
                trap_num = 0
                for i in range(9):
                    near_x = (w_index % size) + ((i % 3) - 1)
                    near_y = (w_index // size) + ((i // 3) - 1)
                    if(near_x < 0 or near_y < 0 or near_x >= size or near_y >= size):
                        continue
                    elif(reverse_board[near_y][near_x] == WALL):
                        trap_num += 1
                        if(trap_num >= 2):
                            break
                else:
                    reverse_board[w_index // size][w_index % size] = WALL
                    break
    

    candidates = []
    for j in range(9):
        x = 3 + (j % 3) - 1
        y = 3 + (j // 3) - 1
        if(reverse_board[y][x] == 0):
            candidates.append([y,x])
    if(len(candidates) > 5):
        candidates = random.sample(candidates, 5)
    for pos in candidates:
        reverse_board[pos[0]][pos[1]] = RTRAP

    for b in range(trap):
        while(True):
            t_index = random.randrange(size*size)
            if(reverse_board[t_index // size][t_index % size] == 0 and t_index != 21 and t_index != 27):
                reverse_board[t_index // size][t_index % size] = RTRAP
                break

    return reverse_board

def MaskBoard(size, item, board):
    mask = [[0 for x in range(size)] for y in range(size)]
    for a in range(item):
        while(True):
            index = random.randrange(size*size)
            if(mask[index // size][index % size] == 0 and board[index // size][index % size] != WALL):
                mask[index // size][index % size] = ITEM
                break
    
    return mask

def ReverseMaskBoard(size):
    mask = [[0 for x in range(size)] for y in range(size)]
    return mask