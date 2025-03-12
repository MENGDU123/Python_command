import threading #多线程库
import time #时间库

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
print("将在10s后执行主程序",end="")
for _ in range(10):
    print(".",end="")
    time.sleep(1)
print()

from function import command1
command1()