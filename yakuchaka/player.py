"""
Playerクラス
"""
import random
import sys
import platform

from .constants import RED, YELLOW, RESET, WALL
from .story import HowToPlay

# プラットフォーム判定とモジュールのインポート
PLATFORM = platform.system()

if PLATFORM == "Windows":
    import msvcrt
else:
    import tty
    import termios


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
            
            # ESCシーケンス(矢印キー)の処理
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
        self.max_hp = hp
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
        puls = random.randrange(1, 4)
        self.movement += puls
        if self.only_one:
            self.movement = 1
            self.only_one = False

        print(YELLOW + f"{self.movement}" + RESET + "が出た!")
        if self.minus_three > 0:
            self.movement -= 3
            self.avoid_trap = True
            if self.movement <= 0:
                self.movement = -1
            self.minus_three -= 1
            print(RED + "トラップの効果で出目が-3された!" + RESET)
    
    # アイテムを使うメソッド。アイテムごとに処理を分けて実装している
    def UseItem(self, index, board):
        if self.items[index] == 1:
            print("HPを全回復した!")
            self.hp = self.max_hp
            del self.items[index]
        elif self.items[index] == 2:
            print("このターン踏んだトラップを無効化!")
            self.avoid_trap = True
            del self.items[index]
        elif self.items[index] == 3:
            print("このアイテムは自動発動なので使用できない")
        elif self.items[index] == 4:
            print("最大HPが5アップ!")
            self.max_hp += 5
            del self.items[index]
        elif self.items[index] == 5:
            print("1マス移動!(ターンを消費しない)")
            self.Move(board)
            del self.items[index]
        
    def Move(self, board):
        print("移動方向を入力(矢印キーで方向決定)")
        while True:
            key = get_arrow_key()
            
            if key is None:
                continue
            
            if key == 'UP':
                if self.y > 0:
                    if board[self.y - 1][self.x] != WALL:
                        self.y += -1
                        break
                print("その方向には移動できない")
            elif key == 'LEFT':
                if self.x > 0:
                    if board[self.y][self.x - 1] != WALL:
                        self.x += -1
                        break
                print("その方向には移動できない")
            elif key == 'DOWN':
                if self.y < len(board) - 1:
                    if board[self.y + 1][self.x] != WALL:
                        self.y += 1
                        break
                print("その方向には移動できない")
            elif key == 'RIGHT':
                if self.x < len(board[self.y]) - 1:
                    if board[self.y][self.x + 1] != WALL:
                        self.x += 1
                        break
                print("その方向には移動できない")
            elif key == 'INVALID':
                print("無効な入力を検知")

    def Action(self, board):
        print("行動を入力(1-5:アイテム番号 s:ルール説明 それ以外の入力でサイコロ)")
        act = input().strip()
        
        # 数字が入力された場合
        if act.isdigit():
            index = int(act) - 1
            if 0 <= index < len(self.items):
                self.UseItem(index, board)
                print("現在の所持アイテム")
                if len(self.items) == 0:
                    print("なし")
                else:
                    for i in range(len(self.items)):
                        print(f"{i+1}: ", end="")
                        if self.items[i] == 1:
                            print("止血剤: HPを全回復")
                        elif self.items[i] == 2:
                            print("安全靴: このアイテムを使ったターン、罠を無効化")
                        elif self.items[i] == 3:
                            print("親子の絆: 死んだとき、HP1で耐え、ランダムな場所にテレポート")
                        elif self.items[i] == 4:
                            print("ドス: 最大HP上昇")
                        elif self.items[i] == 5:
                            print("セグウェイ: ターンを消費せず1マス移動")
            else:
                print("その番号のアイテムは持っていない")

        # ルール説明
        elif act == "s":
            HowToPlay()

        # 隠しコマンド
        elif act == "wwssadadba":
            print("隠しコマンドを確認")
            self.max_hp = 9999
            self.hp = 9999

        # それ以外(サイコロ)
        else:
            self.RollDice()