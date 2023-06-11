# オブジェクト指向 練習

import random

# Userクラス
class User:
    # コンストラクタ
    def __init__(self,name):
        self.name = name     # プレイヤーネーム
        self.hands = 2       # 現在の手の数
        self.thumbs = 0      # 挙げる指の数
        self.estimation = 0  # 予想する数

    # 挙げる指の数を決める
    def decision_thumbs_number(self):
        # 無限ループ発生
        while True:
            # 挙げる指の数を入力させ、入力値をint型に変換して変数に代入
            num = int(input("挙げる指の本数を入力してください："))
            # 入力値が正しい範囲(0から自身の手の数まで)なら
            if num >= 0 and num <= self.hands:
                # 入力値をthumbsプロパティにセット
                self.thumbs = num
                # 無限ループを抜ける
                break
            # 入力値が正しくない
            else:
                print("0~",self.hands,"までの数値で入力してください。")

    # 予想する数を決める
    def decision_estimate_number(self,total_hands): # 引数に両者の手の合計を受け付ける
        # 無限ループ発生
        while True:
            # 予想する指の数の合計本数を入力させ、入力値をint型に変換して変数に代入
            num = int(input("予想する数を入力してください:"))
            # 入力値が正しい範囲 (自身が挙げる指の数以上 かつ 相手が挙げられる最大の指の数＋自身が挙げる指の数まで)なら
            if num >= self.thumbs and num <= total_hands - self.hands + self.thumbs:
                # 入力値をestimationプロパティにセット
                self.estimation = num
                # 無限ループをぬける
                break
            # 入力値が正しくない
            else:
                print(self.thumbs,"～",total_hands-self.hands+self.thumbs,"までの数値で入力してください。")

    
# Computerクラス
class Computer():

    def __init__(self,name):
        self.name = name
        self.hands = 2
        self.thumbs = 0
        self.estimation = 0 

    # 挙げる指の数を決める (ランダム)
    def decision_thumbs_number(self):
        # 0から手の数までのランダム値をthumbsプロパティにセット
        self.thumbs = random.randint(0,self.hands)

    # 予想する数を決める
    def decision_estimate_number(self,total_hands):
        # 自身が挙げる指の数以上 かつ 相手が挙げられる最大の指の数＋自身が挙げる指の数までのランダム値をestimationプロパティにセット
        self.estimation = random.randint(self.thumbs,total_hands - self.hands + self.thumbs)

# 実行するゲーム
def game():

    name = input("プレイヤーネームを入力してください：")
    # Userクラスのインスタンスを生成
    user = User(name)
    # Computerクラスのインスタンスを生成
    com = Computer("コンピューター")

    # 両インスタンスをリストに格納
    members = [user, com] # members[0]がuser、members[1]がcom

    # 10回繰り返す 変数iには0~9がカウントされていく
    for i in range(10):

        # 両インスタンスの現在のhandsプロパティを合計し変数に格納
        total_hands = members[0].hands + members[1].hands

        # 現在何ターン目かを表示
        print("-----",i+1,"ターン目-----")

        # iを2で割ったあまりは0か1になる
        print(members[i%2].name,"のターンです。")

        # 両者が挙げる指の合計を保持する変数
        total_thumbs = 0
        # ユーザーとコンピューターを順番に処理
        for member in members:
            # 挙げる指の数を決めさせる
            member.decision_thumbs_number()

            # 挙げる指の数を合計用変数に格納
            total_thumbs += member.thumbs

        # 予想する数を決めさせる 引数には両者の手の合計を渡す
        members[i%2].decision_estimate_number(total_hands)

        print("------結果------")

        # 両者の挙げた本数や親プレイヤーの予想本数を表示
        print(members[0].name,"は指を",members[0].thumbs,"本挙げました。")
        print(members[1].name,"は指を",members[1].thumbs,"本挙げました。")
        print("挙げられた指の合計本数は",total_thumbs,"本でした。")
        print("予想した本数は",members[i%2].estimation,"本です。")

        # 予想が当たった場合
        if members[i%2].estimation == total_thumbs:
            # 手の数を減らす
            members[i%2].hands -= 1
            print(members[i%2].name,"の予想が当たりました！")

            # 手の数が0になったら
            if members[i%2].hands == 0:
                print(members[i%2].name,"の勝利です！") 
                # ゲーム終了
                return

        else:
            print(members[i%2].name,"の予想は外れました。")

    print("引き分けです")

# Pythonファイル実行時にgame関数から処理を開始させる
if __name__ == "__main__":
    game()

