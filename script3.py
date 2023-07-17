# オブジェクト指向 練習

import random
import pymysql

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
                return members[i%2].name #親プレイヤーの名前を返す

        else:
            print(members[i%2].name,"の予想は外れました。")

    print("引き分けです")

    return "draw"

#ランキングを表示する
def show_ranking(connection):

    #cursorオブジェクトを取得(SQLの実行や結果の取得などができる)
    with connection.cursor() as cursor:

        # SELECT文:resultテーブルからnameカラムとcntカラムを取得(cntカラムの降順に並べ替え5件まで)
        # ORDER BY 列名 ASC(昇順)/DESC(降順)
        # LIMIT 取得件数
        sql = "SELECT name,cnt FROM results ORDER BY cnt DESC LIMIT 5"
        cursor.execute(sql) #SQL実行

        # SELECT文の実行結果を取り出す
        # listの各要素に各レコードがDictionary形式で取得される
        # results = [{name:値,cnt:値},{name:値,cnt:値},{name:値,cnt:値},...]
        results = cursor.fetchall()

    #ランキングが存在しない場合の処理
    if len(results) == 0:
        print("ランキングデータはありません")
        return # 関数を終了
    
    # 見出しの表示
    print("rank Name Count")
    print("--------------------------")

    rank = 1 # 順位表示用変数
    # 取得したレコードを順に表示
    for result in results: # result = {name:値,cnt:値}
        # Dictionaryオブジェクトのgetメゾット => 引数のkeyに対するvalueを取得する
        print(str(rank) + "位 ", result.get("name"), " ", result.get("cnt"))
        rank = rank + 1 #次のレコードの順位

    answer = input("全ランキングを削除しますか？(Y:削除 / Y以外:終了) :")
    if answer == "Y" or answer == "y":
        # ランキングの削除
        delete_ranking(connection)

# ランキングを削除する
def delete_ranking(connection):
    with connection.cursor() as cursor:
        sql = "DELETE FROM results"
        cursor.execute(sql) # SQL実行
        print("ランキングデータを削除しました")
        connection.commit() # 実行結果保存

# ランキングを登録する
def regist_ranking(connection, name):

    with connection.cursor() as cursor:
        # nameカラムの値が、引数で受け付けたユーザー名と一致するレコードを取得
        sql = "SELECT * FROM results WHERE name='"+ name + "'"
        cursor.execute(sql) # SQL実行

        # SELECT文の実行結果を取り出す
        results = cursor.fetchall()

        # SELECT文の実行結果が0件の場合 => 新規プレイヤー
        if len(results) == 0:
            # resultsテーブルにレコードを新規登録
            sql = "INSERT INTO results SET name='" + name + "'"
            # sql = "INSERT INTO results SET name='" + name + "',cnt=1

def main():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1374",
        db="pyapp",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor, #SELECT文の結果をDictionary型で受け取るための記述
    )

    #メニューの表示
    print("------指スマ！！------")
    print("ランキングを見る：0")
    print("ゲームを開始する：1")
    print("終了する：0か1以外")
    answer = input("> ")

    if answer == "0":
        #ランキングの表示
        show_ranking(connection)

    elif answer == "1":
        #game関数を呼び出す
        #戻り値として、ユーザーの名前 or "コンピューター" or "draw"が返る
        winner = game()
        #ユーザーが勝利した場合
        if winner != "コンピューター" and winner != "draw":
            #ランキングの登録/更新
            regist_ranking(connection,winner)
    
    #MySQLとの接続を終了
    connection.close()

# Pythonファイル実行時にgame関数から処理を開始させる
if __name__ == "__main__":
    main()

