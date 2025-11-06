import random
from .constants import ITEM, HEAL, TRAP, RTRAP, DTRAP, WALL
from .enemy import Enemy

def ShowBoard(board, mask, player, enemys):

    print("-----------------------------")
    for y in range(len(board)):
        print("|",end="")
        for x in range(len(board[y])):
            if(x == 0 and y == 3 and player.chaka == True):
                print(" G |",end="")
                continue
            if(player.x == x and player.y == y):
                print(" P |",end="")
            else:
                for enemy in enemys:
                    if(enemy.x == x and enemy.y == y):
                        print(f"{enemy.hp:03d}|",end="")
                        break
                else:
                    if(mask[y][x] == ITEM):
                        print(" ? |",end="")
                    elif(board[y][x] == HEAL):
                        print(" H |",end="")
                    elif(board[y][x] == TRAP and mask[y][x] == 2):
                        print(" T |",end="")
                    elif(board[y][x] == RTRAP):
                        print(" T |",end="")
                    elif(board[y][x] == DTRAP):
                        print(" D |",end="")
                    elif(board[y][x] == WALL):
                        print(" X |",end="")
                    else:
                        print("   |",end="")
        print("")
        print("-----------------------------")

def GetItem(player):
    if(len(player.items) == 5):
        print("持ち物がいっぱいだったので、アイテムを焼いた")
    else:
        percent = random.randrange(100)
        if(percent < 10):
            print("「親子の絆」を手に入れた")
            player.items.append(3)
        elif(percent < 40):
            print("「止血剤」を手に入れた")
            player.items.append(1)
        elif(percent < 60):
            print("「ドス」を手に入れた")
            player.items.append(4)
        elif(percent < 80):
            print("「安全靴」を手に入れた")
            player.items.append(2)
        else:
            print("「セグウェイ」を手に入れた")
            player.items.append(5)

def SummonEnemy(player, index, board, enemys):
    if(index == 2):
        h = (int)(player.max_hp * 1.2)
        while(True):
            x = random.randrange(len(board))
            y = random.randrange(len(board))
            if(board[y][x] != WALL and y != player.y and x != player.x):
                for e in enemys:
                    if(e.x == x and e.y == y):
                        break
                else:
                    return Enemy(h, x, y)
    elif(index == 3):
        return Enemy(50, 6, 3)
    elif(index == 4):
        return Enemy(999, 6, 3, True)
    else:
        percent = random.randrange(5, 10)
        h = (int)(player.max_hp * percent * 0.1)
        while(True):
            x = random.randrange(len(board))
            y = random.randrange(len(board))
            if(board[y][x] != WALL and y != player.y and x != player.x):
                for e in enemys:
                    if(e.x == x and e.y == y):
                        break
                else:
                    return Enemy(h, x, y)
                
def ShowStatus(player):
    print(f"現在のHP {player.hp}/{player.max_hp}")
    print("現在の所持アイテム")
    if(len(player.items) == 0):
        print("何も持っていません")
    else:
        for i in range(len(player.items)):
            print(f"{i+1}: ", end="")
            if(player.items[i] == 1):
                print("止血剤: HPを全回復")
            elif(player.items[i] == 2):
                print("安全靴: このアイテムを使ったターン、罠を無効化")
            elif(player.items[i] == 3):
                print("親子の絆: 死んだとき、HP1で耐え、ランダムな場所にテレポート")
            elif(player.items[i] == 4):
                print("ドス: 最大HP上昇")
            elif(player.items[i] == 5):
                print("セグウェイ: ターンを消費せず1マス移動")

def Trap(player, enemys, board):
    if(board[player.y][player.x] == TRAP):
        print("トラップを踏んでしまった!")
        percent = random.randrange(1, 6)
        damage = int(player.hp * percent * 0.1)
        player.hp -= damage
        print(f"{damage}ダメージ受けた!")

    elif(board[player.y][player.x] == RTRAP):
        print("トラップを踏んでしまった!")
        effect = random.randrange(1,5)
        if(effect == 1):
            player.only_one = True
            print("次のサイコロの出目が1に固定された!")
        elif(effect == 2):
            player.hp -= int(player.max_hp * 0.5)
            print(f"{int(player.max_hp * 0.5)}ダメージ受けた!")
        elif(effect == 3):
            if(len(enemys) == 0):
                print("しかし何も起こらなかった!")
            else:
                enemys[0].Move(board)
                print("自衛隊が1マス近づいてきた!")
        elif(effect == 4):
            if(player.y > 3):
                candidates = [[1, 0],[0, 1],[1, 1]]
                for pos in candidates:
                    if(player.y + pos[0] < 7 or player.x + pos[1] < 7):
                        if(board[player.y + pos[0]][player.x + pos[1]] != WALL):
                            print("ゴールから少し遠ざかってしまった!")
                            player.y += pos[0]
                            player.x += pos[1]
                            break
                else:
                    print("しかし何も起こらなかった!")
            elif(player.y < 3):
                candidates = [[-1, 0],[0, 1],[-1, 1]]
                for pos in candidates:
                    if(player.y + pos[0] >= 0 or player.x + pos[1] < 7):
                        if(board[player.y + pos[0]][player.x + pos[1]] != WALL):
                            print("ゴールから少し遠ざかってしまった!")
                            player.y += pos[0]
                            player.x += pos[1]
                            break
                else:
                    print("しかし何も起こらなかった!")
            elif(player.y == 3):
                candidates = [[0, 1],[1, 1],[-1, 1]]
                for pos in candidates:
                    if(player.x + pos[1] < 7):
                        if(board[player.y + pos[0]][player.x + pos[1]] != WALL):
                            print("ゴールから少し遠ざかってしまった!")
                            player.y += pos[0]
                            player.x += pos[1]
                            break
                else:
                    print("しかし何も起こらなかった!")
            
    elif(board[player.y][player.x] == DTRAP):
        print("強力なトラップを踏んでしまった!")
        effect = random.randrange(5,8)
        if(effect == 5):
            while(True):
                index = random.randrange(49)
                y = index // 7
                if(y >= 2 and y <= 4):
                    continue
                x = index % 7
                if(board[y][x] != WALL):
                    if(len(enemys) != 0):
                        if(y == enemys[0].y and x == enemys[0].x):
                            continue
                    player.y = y
                    player.x = x
                    print("どこかにテレポートしてしまった!")
                    break
        elif(effect == 6):
            player.minus_three = 2
            print("2ターン後までサイコロの出目が-1されるようになった!")
        elif(effect == 7):
            damage = int(player.max_hp * 0.9)
            player.hp -= damage
            print(f"{damage}ダメージ受けた!")

def WinChecker(player):
    if(player.chaka == True and player.x == 0 and player.y == 3):
        return 1
    elif(player.hp <= 0):
        return -1
    else:
        return 0

def Teleport(player, board, enemys):
    while(True):
        index = random.randrange(49)
        y = index // 7
        if(y >= 2 and y <= 4):
            continue
        x = index % 7
        if(board[y][x] != WALL):
            if(len(enemys) != 0):
                if(y == enemys[0].y and x == enemys[0].x):
                    continue
            player.y = y
            player.x = x
            print("どこかにテレポートしてしまった!")
            break