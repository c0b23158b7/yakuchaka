import random
import sys
import platform

# プラットフォーム判定とモジュールのインポート
PLATFORM = platform.system()

if PLATFORM == "Windows":
    import msvcrt
else:
    import tty
    import termios

ITEM = 1
HEAL = 2
TRAP = 3
RTRAP = 4
DTRAP = 5
FLAG = 6
WALL = -1

GAME_ENDER = 0

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'


def get_arrow_key():
    """
    クロスプラットフォーム対応の矢印キー入力取得関数
    Windows: msvcrt使用
    Mac/Linux: termios使用
    
    Returns:
        str: 'UP', 'DOWN', 'LEFT', 'RIGHT', 'INVALID' のいずれか
    """
    if PLATFORM == "Windows":
        # Windows環境
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 224:  # 矢印キーのプレフィックス
                key = ord(msvcrt.getch())
                if key == 72:
                    return 'UP'
                elif key == 80:
                    return 'DOWN'
                elif key == 75:
                    return 'LEFT'
                elif key == 77:
                    return 'RIGHT'
            return 'INVALID'
        return None
    else:
        # Mac/Linux環境
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # ESCシーケンス（矢印キー）の処理
            if ch == '\x1b':  # ESC
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':
                        return 'UP'
                    elif ch3 == 'B':
                        return 'DOWN'
                    elif ch3 == 'C':
                        return 'RIGHT'
                    elif ch3 == 'D':
                        return 'LEFT'
            return 'INVALID'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class Player:
    # Playerの状態を管理する
    def __init__(self, hp, x, y):
        self.max_hp =hp
        self.hp = hp
        self.x = x
        self.y = y
        self.items = []
        self.movement = 0
        self.avoid_trap = False
        self.only_one = False
        self.minus_three = 0
        self.chaka = False
    
    # サイコロを振るメソッド(効果で出目に手が加わる時の処理あり)
    def RollDice(self):
        puls = random.randrange(1,4)
        self.movement += puls
        if(self.only_one == True):
            self.movement = 1
            self.only_one = False

        print(f"「{self.movement}」が出た!")
        if(self.minus_three > 0):
            self.movement -= 3
            if(self.movement <= 0):
                self.movement = -1
            self.minus_three -= 1
            print("トラップの効果で出目が-3された!")
    
    # アイテムを使うメソッド。アイテムごとに処理を分けて実装している
    def UseItem(self, index, board):
        if(self.items[index] == 1):
            print("HPを全回復した!")
            self.hp = self.max_hp
            del self.items[index]
        elif(self.items[index] == 2):
            print("このターン踏んだトラップを無効化!")
            self.avoid_trap = True
            del self.items[index]
        elif(self.items[index] == 3):
            print("このアイテムは自動発動なので使用できない")
        elif(self.items[index] == 4):
            print("最大HPが5アップ!")
            self.max_hp += 5
            del self.items[index]
        elif(self.items[index] == 5):
            print("1マス移動!(ターンを消費しない)")
            self.Move(board)
            del self.items[index]
        
    def Move(self, board):
        print("移動方向を入力(矢印キーで方向決定)")
        while(True):
            key = get_arrow_key()
            
            if key is None:
                continue
            
            if key == 'UP':
                if(self.y > 0):
                    if(board[self.y - 1][self.x] != WALL):
                        self.y += -1
                        break
                print("その方向には移動できない")
            elif key == 'LEFT':
                if (self.x > 0):
                    if(board[self.y][self.x - 1] != WALL):
                        self.x += -1
                        break
                print("その方向には移動できない")
            elif key == 'DOWN':
                if(self.y < len(board) - 1):
                    if(board[self.y + 1][self.x] != WALL):
                        self.y += 1
                        break
                print("その方向には移動できない")
            elif key == 'RIGHT':
                if(self.x < len(board[self.y]) - 1):
                    if(board[self.y][self.x + 1] != WALL):
                        self.x += 1
                        break
                print("その方向には移動できない")
            elif key == 'INVALID':
                print("無効な入力を検知")
        
    def Action(self, board):
        while(True):
            print("行動を入力(i:アイテム s:ルール説明 それ以外の入力でサイコロ)")
            act = input().strip()
            if(act == "i"):
                if(len(self.items) == 0):
                    print("アイテムを所持していません")
                else:
                    print("使用するアイテムの番号を入力してください")
                    correct_input = []  # 存在するアイテム番号の文字列を格納するためのリスト
                    for i in range(len(player.items)):
                        correct_input.append(str(i+1))  # 番号の文字列を追加
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
                    use = input().strip()
                    if(use in correct_input):  # 入力された文字が正しい番号であるかの確認
                        self.UseItem(int(use)-1, board)
                        break
                    else:
                        print("無効な入力です")
                        return
            elif(act == "s"):
                HowToPlay()
                break
            elif(act == "wwssadadba"):
                print("隠しコマンドを確認")
                self.max_hp = 9999
                self.hp = 9999
            else:
                self.RollDice()
                return

class Enemy:
    def __init__(self, hp, x, y, dd = False):
        self.hp = hp
        self.x = x
        self.y = y
        self.devilsdog = dd
    
    def Battle(self, index, player):
        print("敵と遭遇した!")
        if(player.hp <= self.hp):
            player.hp = 0
            print("負けてしまった...")
        else:
            if(index == 3):
                print("ボスを倒した!")
                print("チャカ(銃)を手に入れた!")
                player.chaka = True
                drop = random.randrange(4)
                if(drop != 3):
                    print("アイテムを落とした!")
                    GetItem(player)
            else:
                print("敵を倒した!")
                if(index == 2):
                    drop = random.randrange(2)
                else:
                    drop = random.randrange(4)
                if(drop == 0):
                    print("アイテムを落とした!")
                    GetItem(player)
            upper = int(self.hp / 2.0)
            damage = int(self.hp / 4.0)
            player.max_hp += upper
            player.hp -= damage
            print(f"最大HPが「{upper}」上昇した!")
            print(f"この戦闘で「{damage}」ダメージ受けた")
                
    def SearchBattle(self, index, player):
        if(self.x == player.x and self.y == player.y):
            player.movement = 0
            self.Battle(index, player)
            return 1
        else:
            return 0

    # 行動の変更点(Aiの活用+行動ごとにエンターキーを入力することで進行)
    def Move(self, board, player):
        print("敵の行動: Enterでページ送り")
        st = input()
        pf = PathFinding()
        moving = pf.get_next_move(board, [self.y, self.x], [player.y, player.x])
        if moving is not None:
            self.y = moving[0]
            self.x = moving[1]

class Node:    
    #クラスの初期化。最初のノードは親もない、場所もない。
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0
        self.h = 0
        self.f = 0

class PathFinding:
    """
    A*探索を使うAIのクラス
    ゲームボード上での最短経路を探索し、次の行動を決定する
    """
    def __init__(self):
        self.queue = None           # 待ち行列
        self.visited = []           # 訪問済みの場所
        self.path = []              # ゴールまでの経路
        self.cost = 0               # 見つけった経路のコスト
        self.search_name = "A* Search"

    def find_path(self, board, start, goal):
        """
        迷路のスタートノードからゴールノードまでの経路を作成
        
        Args:
            board: ゲームボード(2次元リスト)
            start: スタート位置 [y, x]
            goal: ゴール位置 [y, x]
        
        Returns:
            bool: 経路が見つかった場合True、見つからなかった場合False
        """
        # スタートノードとゴールノードを作成(クラスを使用)と深さを初期化
        start_node = Node(None, start)
        start_node.depth = 0
        goal_node = Node(None, goal)
        goal_node.depth = 0
        
        # まだ訪問されていないノードと既に訪問されたノードを初期化。
        self.queue = []
        self.visited = []
        # スタートノードはまだ訪問されていないので未訪問リストに保存
        self.queue.append(start_node)
        
        # 2次元の迷路の可能な移動
        move = [[-1, 0],    # 上
                [0, -1],    # 左
                [1, 0],     # 下
                [0, 1]]     # 右
        
        # 迷路の行と列の数を把握
        row_no = len(board)
        column_no = len(board[0])
        
        # ゴールノードを発見するまでのループ(まだ訪問されていないノードがある限る続く)
        while len(self.queue) > 0:
            # fコストが一番低いノードは次に展開する
            current_node = self.queue[0]
            current_index = 0
            for index, item in enumerate(self.queue):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # 選んだノードをまだ訪問されていないリストから削除、既に訪問されたノードに追加
            self.queue.pop(current_index)
            # 次に展開するノードを既に訪問されたノードに追加
            self.visited.append(current_node)
            
            # 展開のために選んだノードはゴールノードならば探索終了
            if current_node.position == goal_node.position:
                self.path = self._return_path(current_node)
                self.cost = current_node.g
                return True
            
            # ノードを展開する。全ての可能な行動を把握。この迷路ゲームの場合、4つ方向は可能(上、左、下、右)
            # 可能な移動先のノードを保存するためのリストを初期化
            children = []
            for new_position in move:
                # 次の場所を把握
                node_position = [current_node.position[0] + new_position[0],
                                current_node.position[1] + new_position[1]]
                # 迷路から出ていないことを確認
                if (node_position[0] > (row_no - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (column_no - 1) or
                    node_position[1] < 0):
                    continue
                
                # 壁の確認
                if board[node_position[0]][node_position[1]] == WALL:
                    continue
                
                # 可能な移動先。その移動先のノードを作成
                new_node = Node(current_node, node_position)
                
                # 可能な移動先のノードを保存(リストに追加)
                children.append(new_node)
    
            # 全ての作成された移動先のノードに対して、既に訪問されたかどうか、未訪問ノードの中に既にあるかどうかを確認
            for child_node in children:
                # 子ノードの場所は既に訪問されたら追加しない
                for visited_node in self.visited:
                    if child_node.position == visited_node.position:
                        break
                else:               
                    # f、g、とhの値を計算
                    child_node.g = self._get_path_cost(current_node, child_node)
                    child_node.h = self._get_heuristic_cost(child_node, goal_node)
                    child_node.f = child_node.g + child_node.h
                        
                    # まだ訪問されていないノードの中に同じノードがあるかどうか
                    add_to_queue = True
                    for node in self.queue:
                        if child_node.position == node.position:
                            # 現在のノードが以前のノードより良い経路であらばノード情報を更新
                            if node.g > child_node.g:
                                node.g = child_node.g
                                node.f = child_node.f
                                node.parent = current_node
                            # 同じ場所を表しているノードが待ち行列に既にあるならば追加しない
                            add_to_queue = False
                    if add_to_queue:
                        self.queue.append(child_node)
        
        # 経路が見つからなかった場合
        return False

    def _get_path_cost(self, parent, child):
        """
        経路コストを計算
        このゲームでは全ての移動コストを1とする
        """
        return parent.g + 1

    def _get_heuristic_cost(self, child, goal):
        """
        ヒューリスティック距離を計算。この例、Manhattan距離を計算する
        """
        return abs(child.position[0] - goal.position[0]) + abs(child.position[1] - goal.position[1])

    def _return_path(self, node):
        """
        探索が成功した場合、スタートノードからゴールノードまでの経路を作成
        """
        # 出力経路リストの初期化
        path = []
        current = node
        # 現在のノードはスタートまで(親はNone)に迷路の場所(position)を保存
        while current is not None:
            path.append(current.position)
            current = current.parent
        # 作成した経路はゴールノードからスタートノードまでなので逆方向にする
        path = path[::-1]
        # 戻り値は作成した経路
        return path

    def get_next_move(self, board, start, goal):
        """
        次の移動先を取得する
        
        Args:
            board: ゲームボード(2次元リスト)
            start: スタート位置 [y, x]
            goal: ゴール位置 [y, x]
        
        Returns:
            list or None: 次の移動先 [y, x]、経路が見つからない場合はNone
        """
        # 経路を探索
        if self.find_path(board, start, goal):
            # 経路が見つかった場合、次の移動先を返す
            # path[0]はスタート地点なので、path[1]が次の移動先
            if len(self.path) > 1:
                return self.path[1]
            else:
                # すでにゴールにいる場合
                return start
        else:
            # 経路が見つからなかった場合
            return None

    def get_full_path(self):
        """
        最後に見つけた経路全体を取得
        
        Returns:
            list: 経路のリスト
        """
        return self.path

    def get_path_cost(self):
        """
        最後に見つけた経路のコストを取得
        
        Returns:
            int: 経路のコスト
        """
        return self.cost


def MakeBoard(size, trap, heal):
    board = [[0 for x in range(size)] for y in range(size)]

    wall_pos = [16, 18, 30, 32]
    for b in range(4):
            w_index = wall_pos[b]
            if(board[w_index // size][w_index % size] == 0):
                board[w_index // size][w_index % size] = WALL

    for a in range(trap):
        while(True):
            t_index = random.randrange(size*size)
            if(board[t_index // size][t_index % size] == 0):
                board[t_index // size][t_index % size] = TRAP
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

    while(True):
        regen = False
        w_candidates = []
        for a in range(wall):
            while(True):
                w_index = random.randrange(size*size)
                if(w_index not in w_candidates and w_index != 21 and w_index != 27):
                    w_candidates.append(w_index)
                    break
        for pos in w_candidates:
            c_num = 0
            for i in range(9):
                y_dif = (i // 3 - 1) * 7
                x_dif = (i % 3 - 1)
                if(pos + y_dif + x_dif in w_candidates):
                    c_num += 1
                    if(c_num >= 3):
                        regen = True
                        break
            if(regen == True):
                break
        if(regen != True):
            break
    for spot in w_candidates:
        reverse_board[spot // size][spot % size] = WALL

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

def ShowBoard(board, mask, player, enemys):

    print("-----------------------------")
    for y in range(len(board)):
        print("|",end="")
        for x in range(len(board[y])):
            if(x == 0 and y == 3 and player.chaka == True):
                print(" G |",end="")
                continue
            if(player.x == x and player.y == y):
                print(GREEN + " P " + RESET + "|",end="")
            else:
                for index in range(len(enemys)):
                    if(enemys[index].x == x and enemys[index].y == y):
                        if(enemys[index].devilsdog or index == 2):
                            print(RED+ f"{enemys[index].hp:03d}" + RESET + "|",end="")
                            break
                        elif(index == 3):
                            print(YELLOW + f"{enemys[index].hp:03d}" + RESET + "|", end="")
                            break
                        else:
                            print(f"{enemys[index].hp:03d}|",end="")
                            break
                else:
                    if(mask[y][x] == ITEM):
                        print(" ? |",end="")
                    elif(board[y][x] == HEAL):
                        print(" ✙ |",end="")
                    elif(board[y][x] == TRAP and mask[y][x] == 2):
                        print(" T |",end="")
                    elif(board[y][x] == RTRAP):
                        print(" T |",end="")
                    elif(board[y][x] == DTRAP):
                        print(" D |",end="")
                    elif(board[y][x] == WALL):
                        print(" ▪ |",end="")
                    else:
                        print("   |",end="")
        print("   ",end="")
        if(player.chaka == True):
            if(y == 2):
                print("▪:壁")
            elif(y == 3):
                print("数字(赤):追跡する敵")
            elif(y == 4):
                print("T:止まるとデメリットが発生するトラップ")
            elif(y == 5):
                print("D:Tよりも強力な効果を持つデストラップ")
            elif(y == 6):
                print("G:ピッタリ止まることでクリアになるゴール")
            else:
                print("")
        else:
            if(y == 0):
                print("▪:壁")
            if(y == 1):
                print("数字(白):止まっている敵")
            if(y == 2):
                print("数字(赤):追跡してくる敵")
            if(y == 3):
                print("数字(黄):チャカを持っている警官")
            if(y == 4):
                print("✙:通過することでHPを全回復する(何度でも使用可能)")
            if(y == 5):
                print("?:通過することでランダムにアイテムを獲得")
            if(y == 6):
                print("T:すでに発動したトラップ(もう効果を発動しない)")
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
        if(h >= 500):
            h = 500
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
        if(h >= 500):
            h = 500
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
        print("")
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
                enemys[0].Move(board, player)
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

def Story():
    story = ["大阪を拠点とするヤクザグループ、紅白組。そこの新入りヤクザは組長からある命令を言い渡された。",
             "組長「おう新入り、今度の抗争はかなり激しくなりそうや。」",
             "組長「そこでお前には梅田駅にいるサツからチャカ盗ってきて欲しいんや。」",
             "組長「これができりゃお前を一人前と認めたる。どうや、出来るやろ?」",
             "こうして、新入りヤクザのあなたは梅田駅の警察から拳銃を奪うため、夜の大阪に踏み出した!",
             "",
             "警視庁「今夜、紅白組の下っ端が梅田駅で一般人を襲撃するという情報を得た",
             "警視庁「現場の警官は銃を携帯の上、厳重に警戒したまえ",
             "警視庁「また、有事の際には自衛隊の第一空挺団員と迅速に連携を取れるように手筈を整えておく",
             "チャカを賭けた漢の仁義なき闘争が今、始まる!!"]
    
    print("---------------------ストーリー---------------------(Enterでページ送り,sでスキップ)")
    for p in range(0, len(story), 3):
        for index in range(3):
            if(p+index >= len(story)):
                break
            print(story[p+index])
        st = input().strip()
        if(st == "s"):
            break

def HowToPlay():
    how = [YELLOW + "行動" + RESET + ":ターン開始時、iキーを入力することでアイテム使用モードに移行する",
           "sキーを入力することで再びこのチュートリアルを見ることができる",
           "アイテム使用モードでは所持アイテムの番号を入力することでそのアイテムを使用できる",
           "i、s以外の入力(無を含む)を行うことでサイコロをふることができる",
           "サイコロは1~3の出目があり、出目の数だけ移動する",
           "移動には矢印キーを使う(移動の入力はEnter不要)",
           YELLOW + "戦闘" + RESET +"：マップ上の数字は敵のHPを意味し、このマスに接触すると戦闘が始まる",
           "このとき、まだこのターン移動できる回数が残っていても強制的にストップすることになる",
           "戦闘では自身の残りHPが敵のHPより大きければ勝利する",
           "敗北すると死亡となり" + RED + "ゲームオーバー" + RESET,
           "勝利すると敵のHPの1/4分残りHPが減少し、敵のHPの1/2分最大HPが増加する",
           "また、勝利時にランダムで敵がアイテムをドロップする可能性がある",
           YELLOW + "目標" + RESET + ":マップ上の黄色の数字が警官のHPである",
           "この警官を倒せるようになるまで敵と戦い、警官を倒そう",
           "警官を倒した後、" + RED + "梅田駅から脱出することでクリアとなる" + RESET]
    
    print("---------------------チュートリアル---------------------(Enterでページ送り,sでスキップ)")
    for h in range(0,len(how),3):
        for index in range(3):
            if(h+index >= len(how)):
                break
            print(how[h+index])
        s = input().strip()
        if(s == "s"):
            break

def ReverseIntoroduction():
    introduction = [YELLOW + "脱出" + RESET + ":マップ上の左側にあるGがゴール",
                    "ゴールにピッタリ止まることで脱出成功となり、クリアである",
                    "今まであった休憩マスや通常敵は存在しない",
                    YELLOW + "外敵" + RESET + ":今いるマスから3マス分距離を取ると、第一空挺団が出現する",
                    "裏面が始まった時にプレイヤーがいるマスが第一空挺団の初期位置",
                    "第一空挺団はHPが999あり、自分の行動の終わりに1~2マス最短ルートで接近してくる",
                    "また、今までとは異なり、マップ上にトラップが表示されているが、踏むと" + RED + "効果が発動する" + RESET,
                    "一度踏んだトラップであっても再度効果を発動する",
                    "マップ上のDは通常より強力なトラップを意味している。一度踏むだけでアイテムが無ければ" + RED + "打開不能になるほど強力" + RESET]
    
    print("---------------------裏面スタート---------------------(Enterでページ送り,sでスキップ)")
    for h in range(0,len(introduction),3):
        for index in range(3):
            if(h+index >= len(introduction)):
                break
            print(introduction[h+index])
        s = input().strip()
        if(s == "s"):
            break

def NoWayBoard(board, enemys):
    noway = [[0 for a in range(len(board))] for b in range(len(board))]
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == WALL:
                noway[y][x] = WALL
    for en in enemys:
        noway[en.y][en.x] = WALL
    
    return noway


# メインゲームループ
board1 = MakeBoard(7, 4, 2)
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

print(f"検出されたプラットフォーム: {PLATFORM}")
print("矢印キーでの移動が使用できます")
print()

Story()
HowToPlay()

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
                    if(enemys[i].devilsdog):
                        del enemys[i]
                        enemys.insert(i, SummonEnemy(player, 4, board, enemys))
                    else:
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
        if(mask[player.y][player.x] != 2 or player.chaka):
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
            ReverseIntoroduction()
            print("チャカを手に入れた!")
            print("あとは出入り口に戻るだけだ!")
            print("なぜか嫌な予感がする...早く脱出しよう!")
    else:
        for i in range(len(enemys)):
            if(enemys[i].devilsdog == True):
                move = random.randrange(1,4)
                if(move == 3):
                    move = 2
                # 行動回数の表示
                print(f"敵の行動回数:{move}")
                for j in range(move):
                    # Moveメソッドの引数変更
                    noway = NoWayBoard(board, enemys)
                    enemys[i].Move(noway, player)
                    for i in range(len(enemys)):
                        battle = enemys[i].SearchBattle(i, player)
                        if(battle == 1):
                            if(enemys[i].devilsdog):
                                del enemys[i]
                                enemys.insert(i, SummonEnemy(player, 4, board, enemys))
                            else:
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
            
        if(len(enemys) == 0):
            distance = abs(player.x - 6) + abs(player.y - 3)
            if(distance >= 3):
                print("第一空挺団が出現!")
                enemys.append(SummonEnemy(999, 4, board, enemys))
        
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