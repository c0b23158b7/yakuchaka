# -*- coding: utf-8 -*-
"""
A*探索を使った経路探索機能
元のMazeAstarSearch.pyを基にゲーム用に調整
"""

from .constants import WALL

"""
探索木のためのノードクラス
parentは現在のノードを親ノード
positionはノードが表している迷路の場所
gは経路コスト(スタートから現在の場所の移動コスト)
hはヒューリスティックの値(目的までのコストの見積もり)
fは親ノードの合計コスト(f = g + h)
"""
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