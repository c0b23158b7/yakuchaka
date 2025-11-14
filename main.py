import random
from yakuchaka.constants import *
from yakuchaka.player import Player
from yakuchaka.enemy import Enemy
from yakuchaka.board import MakeBoard, MakeReverseBoard, MaskBoard, ReverseMaskBoard
from yakuchaka.game_utils import ShowBoard, GetItem, SummonEnemy, ShowStatus, Trap, WinChecker, Teleport, NoWayBoard
from yakuchaka.story import Story

board1 = MakeBoard(7, 4, 4, 2)
board2 = MakeReverseBoard(7, 7, 10)
mask1 = MaskBoard(7, 2, board1)
mask2 = ReverseMaskBoard(7)
player = Player(15, 0, 3)
enemys = []
nulls = []
reverse = False

for i in range(3,-1, -1):
    enemys.insert(0, SummonEnemy(player, i, board1, enemys))

board = board1
mask = mask1

Story(board, mask, player, enemys)

while(True):
    noway = NoWayBoard(board, enemys)
    while(player.movement == 0):
        ShowBoard(board, mask, player, enemys)
        ShowStatus(player)
        GAME_ENDER = WinChecker(player)
        if(GAME_ENDER == 1):
            break
        elif(GAME_ENDER == -1):
            if(3 in player.items):
                del player.items[player.items.index(3)]
                player.hp = 1
                GAME_ENDER = 0
                Teleport(player, board, enemys)
            else:
                break
        player.Action(board)
    while(player.movement != 0):
        if(player.movement == -1):
            player.movement = 0
        else:
            player.Move(board)
            player.movement -= 1
            for i in range(len(enemys)):
                battle = enemys[i].SearchBattle(i, player)
                if(battle == 1):
                    del enemys[i]
                    enemys.insert(i, SummonEnemy(player, i, board, enemys))
            if(board[player.y][player.x] == HEAL):
                player.hp = player.max_hp
                print("休憩所マスの効果でHPが全回復した!")
            if(mask[player.y][player.x] == ITEM):
                GetItem(player)
                mask[player.y][player.x] = 0
            ShowBoard(board, mask, player, enemys)
            ShowStatus(player)
    GAME_ENDER = WinChecker(player)
    if(GAME_ENDER == 1):
        break
    elif(GAME_ENDER == -1):
        if(3 in player.items):
            del player.items[player.items.index(3)]
            player.hp = 1
            GAME_ENDER = 0
            Teleport(player, board, enemys)
        else:
            break
    if(player.avoid_trap == True):
        player.avoid_trap = False
    else:
        if(mask[player.y][player.x] != 2):
            Trap(player, enemys, board)
    mask[player.y][player.x] = 2
    GAME_ENDER = WinChecker(player)
    if(GAME_ENDER == 1):
        break
    elif(GAME_ENDER == -1):
        if(3 in player.items):
            del player.items[player.items.index(3)]
            player.hp = 1
            GAME_ENDER = 0
            Teleport(player, board, enemys)
        else:
            break
    if(player.chaka == True and reverse == False):
            reverse = True
            enemys.clear()
            board = board2
            mask = mask2
            print("チャカを手に入れた!")
            print("あとは出入り口に戻るだけだ!")
            print("なぜか嫌な予感がする...早く脱出しよう!")
    else:
        if(len(enemys) == 0):
            distance = abs(player.x - 6) + abs(player.y - 3)
            if(distance >= 3):
                enemys.append(SummonEnemy(999, 4, board, enemys))
        for i in range(len(enemys)):
            if(enemys[i].devilsdog == True):
                move = random.randrange(1,4)
                # 行動回数の表示
                print(f"敵の行動回数:{move}")
                for j in range(move):
                    # Moveメソッドの引数変更
                    noway = NoWayBoard(board, enemys)
                    enemys[i].Move(noway, player)
                    for i in range(len(enemys)):
                        battle = enemys[i].SearchBattle(i, player)
                        if(battle == 1):
                            del enemys[i]
                            enemys.insert(i, SummonEnemy(player, i, board, enemys))
                    # 変更点(敵の行動ごとに盤面を表示する)
                    if(j+1 != move):
                        ShowBoard(board, mask, player, enemys)

            elif(i == 2 and enemys[i].hp >= player.hp):
                noway = NoWayBoard(board, enemys)
                # Moveメソッドの引数変更
                enemys[i].Move(noway, player)
                for i in range(len(enemys)):
                    battle = enemys[i].SearchBattle(i, player)
                    if(battle == 1):
                        del enemys[i]
                        enemys.insert(i, SummonEnemy(player, i, board, enemys))
        
        GAME_ENDER = WinChecker(player)
        if(GAME_ENDER == 1):
            break
        elif(GAME_ENDER == -1):
            if(3 in player.items):
                del player.items[player.items.index(3)]
                player.hp = 1
                GAME_ENDER = 0
                Teleport(player, board, enemys)
            else:
                break

            
if(GAME_ENDER == 1):
    print("GAME CLEAR!!")
elif(GAME_ENDER == -1):
    print("GAME OVER")
else:
    print("ERROR!!!")