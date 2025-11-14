import random
from .constants import WALL

class Enemy:
    def __init__(self, hp, x, y, dd = False):
        self.hp = hp
        self.x = x
        self.y = y
        self.devilsdog = dd
    
    def Battle(self, index, player):
        from .game_utils import GetItem
        
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
        from .pathfinding import PathFinding
        
        print("敵の行動: Enterでページ送り")
        st = input()
        pf = PathFinding()
        moving = pf.get_next_move(board, [self.y, self.x], [player.y, player.x])
        if moving is not None:
            self.y = moving[0]
            self.x = moving[1]