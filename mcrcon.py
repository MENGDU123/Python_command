from rcon.source import Client
import time

from config import *


class MCRcon(Client):
    def __init__(self):
        super().__init__(f'{ipadd}', port, passwd=f'{password}')

    def get_scoreboard(self, player):
        response = self.run(f'scoreboard players list {player}')
        scoreboards = ''.join(response.split(':', 1)[1:]).strip()

        scoreboard = {}

        if scoreboards:
            scoreboards = scoreboards.split('[')[1:]

            for score in scoreboards:
                key, value = score.split(']: ')
                scoreboard[key] = int(value)

        return scoreboard

    def interrupt_mode(self):
        while cmd := input():
            print(self.run(cmd))


if __name__ == '__main__':
    with MCRcon() as mr:
        player_scoreboards = mr.get_scoreboard(f'Peter_2500')
        print(player_scoreboards)

        print(f'123计分板的数值是: {player_scoreboards.get('123')}')

        # 示例应用
        kill_count = 0
        # while True:
        #     player_scoreboards = mr.get_scoreboard(f'Peter_2500')
        #     new_kill_count = player_scoreboards.get('kills', 0)
        #     if new_kill_count > kill_count:
        #         print(f"Kill count 增加了 {new_kill_count - kill_count}！现在是 {new_kill_count}")
        #     kill_count = new_kill_count
        #     time.sleep(0.5)


        mr.interrupt_mode()
