#list
# 1.空配列（リストの初期化）
# 変数名：empty_list, 要素：なし
empty_list = []
# コマンドラインへ出力
print(empty_list, type(empty_list))

# 2.整数配列
int_list = [0,1,2]

print(int_list,type(int_list))

# 3.任意の配列宣言
my_list = [4,"ab",6,"cde"]

print(my_list,type(my_list))

# 4.リスト関数を使った初期化
init_list = list()

print(init_list,type(init_list))

# tuple
# 5.タプル
str_tuple=("a","b","c")

print(str_tuple,type(str_tuple))

# 6.タプルからリストを作成
str_list=list(str_tuple)

print(str_list,type(str_list))

# dictionary
# 7.ディクショナリ
dic={"りんご":120, "バナナ":100, "いちご":200}

print(dic,type(dic))

# lem(変数名) -> 要素数の表示
# 変数名.append(要素)　-> 要素の追加
# 変数名.extend(要素,要素,要素) -> 複数の要素の追加
# 変数名.insert(~番目,要素) -> 配列の~番目に要素を追加
# del 変数名[~番目] -> ~番目の要素を削除
# del 変数名[~番目:~番目] -> ex)[3:5] = 3番目から5番目の手前までを削除（3番目と4番目を削除）

# 関数
def main():
    for i in range(40):
        print(FizzBuzz(i+1))
    return 

def FizzBuzz(num):
    if num%3==0 and num%5==0:
        return "FizzBuzz"
    elif num%3==0:
        return "Fizz"
    elif num%5==0:
        return "Buzz"
    else:
        return str(num)
    
if __name__=="__main__":
    main()