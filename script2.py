# 再帰関数
def main():
    print(sum(10))

def sum(n):
    if n <= 0:
        return n
    return n + sum(n-1)

if __name__=="__main__":
    main()