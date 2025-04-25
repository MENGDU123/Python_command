"""
该脚本主要测试服务器连通性（基于ICMP协议）
无法用于禁用广域网ping的主机！
该脚本可以单独运行，也可以在 main 中调用。
IP参数在 config 中设置。
"""
def net():

    from ping3 import ping
    import time

    second = 0 #主机响应时间
    n = 0 #连接尝试次数

    from config import ipadd

    for _ in range(3):
        n = n + 1
        print()
        print(f"正在尝试第{n}次Ping...")
        second = str(ping(ipadd))
        if second == 'False':
            print("Ping失败,稍后将尝试重连……")
            for _ in range(9):
                print(".",end="")
                time.sleep(1)
        else:
            break

    if second == 'False':
        print()
        print("服务器未响应，已终止程序。")
        exit(-1)

    for _ in range(6):
        print(".",end="")
        time.sleep(1)
    print("...成功！")
    second = float(second)
    print(f"服务器响应时间为{second:.2f}s")

net()