import random
from .constants import WALL, HEAL, ITEM

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
        while(True):
            print("移動方向を入力してください(↑:w ←:a ↓:s →:d)")
            act = input().strip()
            if(act == "w"):
                if(self.y > 0):
                    if(board[self.y - 1][self.x] != WALL):
                        self.y += -1
                        break
                print("その方向には移動できない")
            elif(act == "a"):
                if (self.x > 0):
                    if(board[self.y][self.x - 1] != WALL):
                        self.x += -1
                        break
                print("その方向には移動できない")
            elif(act == "s"):
                if(self.y < len(board) - 1):
                    if(board[self.y + 1][self.x] != WALL):
                        self.y += 1
                        break
                print("その方向には移動できない")
            elif(act == "d"):
                if(self.x < len(board[self.y]) - 1):
                    if(board[self.y][self.x + 1] != WALL):
                        self.x += 1
                        break
                print("その方向には移動できない")
            else:
                print("無効な入力を検知")
        
    def Action(self, board):
        while(True):
            print("行動を入力してください")
            print("サイコロ:r")
            print("アイテム:i")
            act = input().strip()
            if(act == "r"):
                self.RollDice()
                break
            elif(act == "i"):
                if(len(self.items) == 0):
                    print("アイテムを所持していません")
                else:
                    print("使用するアイテムの番号を入力してください")
                    for i in range(len(self.items)):
                        print(f"{i+1}: ", end="")
                        if(self.items[i] == 1):
                            print("止血剤: HPを全回復")
                        elif(self.items[i] == 2):
                            print("安全靴: このアイテムを使ったターン、罠を無効化")
                        elif(self.items[i] == 3):
                            print("親子の絆: 死んだとき、HP1で耐え、ランダムな場所にテレポート")
                        elif(self.items[i] == 4):
                            print("ドス: 最大HP上昇")
                        elif(self.items[i] == 5):
                            print("セグウェイ: ターンを消費せず1マス移動")
                    use = int(input())
                    if(use <= len(self.items)):
                        self.UseItem(use-1, board)
                        break
                    else:
                        print("無効な入力です")
                        return
            elif(act == "wwssadadba"):
                print("隠しコマンドを確認")
                self.max_hp = 9999
                self.hp = 9999
            else:
                print("無効な入力です")
                return