"""
该模块功能是外置命令方块，利用 RCON 对服务器发送指令。
"""

import threading #多线程库
import time #时间库
from cgi import print_arguments

print("欢迎使用由梦都开发的远程命令方块，本程序基于RCON协议。")

while True:
    ask = str(input("开始之前，需要进行网络连通性测试吗（Y/n）："))
    if 'Y' in ask:
        print("即将开始Ping目标主机……")
        from network import net
        net()
        break
    elif 'n' in ask:
        print("跳过连通性测试")
        break
    else:
        print("未解析输入。")
        print()

print()
print("将在10s后执行主程序",end="")
for _ in range(10):
    print(".",end="")
    time.sleep(1)
print()

c = 0

while True:
    try:

        from config import greetings
        from config import ipadd
        from config import port
        from config import password

        from rcon.source import Client
        with Client(f'{ipadd}', port, passwd=f'{password}') as client:
            response = client.run(f"say @a {greetings}")
            print(response)

    except ConnectionError:
        c = c + 1
        if c == 4:
            print("重试次数太多，已终止程序。")
            exit(-1)

        print("RCON接入失败，请检查服务端！")
        ask = str(input(f"Press Enter to continue...({c})"))
        print()
        continue

    else:
        break


from function import command1
from function import command2

thread1 = threading.Thread(target=command1())
thread2 = threading.Thread(target=command2())

thread1.start()
thread2.start()

thread1.join()
thread2.join()
