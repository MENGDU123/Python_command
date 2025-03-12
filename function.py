from config import ipadd
from config import port
from config import password



def command1():

    import time

    from rcon.source import Client
    with Client(f'{ipadd}', port, passwd=f'{password}') as client:
        # 扫地机器人模块
        while True:
            response = client.run('tell @a 服务器马上就要扫地啦！')
            print(response)
            t = 5
            for _ in range(5):
                response = client.run(f"say @a {t}")
                print(response)
                t = t - 1
                time.sleep(1)
            response = client.run("kill @e[type=item]")
            print(response)
            time.sleep(60)

def command2():

    from rcon.source import Client
    with Client(f'{ipadd}', port, passwd=f'{password}') as client:

        response = client.run("say @a 服务器已接入RCON")
        print(response)



