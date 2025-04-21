from rcon.source import Client

from config import *


class MCRcon(Client):
    def __init__(self):
        super().__init__(f'{ipadd}', port, passwd=f'{password}')

    def get_scoreboard(self, player: str) -> dict[str, int]:

        response: str = self.run(f'scoreboard players list {player}')
        scoreboards: str = ''.join(response.split(':', 1)[1:]).strip()

        scoreboard: dict[str, int] = {}

        if scoreboards:
            scoreboards_list: list[str] = scoreboards.split('[')[1:]

            for score in scoreboards_list:
                key, value = score.split(']: ')
                scoreboard[key] = int(value)

        return scoreboard

    def get_player(self) -> list[str]:

        players: str = self.run('list').strip()

        player_list: list[str] = players.split(': ', 1)[1:]

        return player_list if not player_list else player_list[0].split(', ')

    def interrupt_mode(self) -> None:
        while cmd := input():
            print(self.run(cmd))


if __name__ == '__main__':
    with MCRcon() as mr:
        player_scoreboards = mr.get_scoreboard(f'Steve')
        print(player_scoreboards)

        print(f'123计分板的数值是: {player_scoreboards.get('123')}')
        print(mr.get_player())

        mr.interrupt_mode()
