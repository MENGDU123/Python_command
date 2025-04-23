from rcon.source import Client
import uuid

from config import *


def java_array_to_uuid(array: list[int]) -> uuid.UUID:
    byte_array = bytearray()
    for item in array:
        unsigned_int = item & 0xFFFFFFFF

        byte_array += unsigned_int.to_bytes(4, byteorder='big', signed=False)

    return uuid.UUID(bytes=bytes(byte_array))


def test_selector(selector, client: Client):
    response = client.run(f'execute if entity {selector}')
    if selector in response:
        return False
    else:
        return True


class MCRcon(Client):
    def __init__(self):
        super().__init__(f'{ipadd}', port, passwd=f'{password}')

    def get_scoreboards(self, player: str) -> dict[str, int]:

        response: str = self.run(f'scoreboard players list {player}')
        scoreboards: str = ''.join(response.split(':', 1)[1:]).strip()

        scoreboard: dict[str, int] = {}

        if scoreboards:
            scoreboards_list: list[str] = scoreboards.split('[')[1:]

            for score in scoreboards_list:
                key, value = score.split(']: ')
                scoreboard[key] = int(value)

        return scoreboard

    def get_uuid(self, selector: str) -> list[uuid.UUID]:
        response: str = self.run(f'execute as {selector} run data get entity @s UUID')
        try:
            split_responses = response.split(']')[:-1]
            uuid_list = [java_array_to_uuid(
                list(map(int, split_response.split('; ')[1].split(', '))))
                for split_response in split_responses
            ]

        except:
            raise Exception(response)

        else:
            return uuid_list

    def get_players(self) -> list[str]:

        players: str = self.run('list').strip()

        player_list: list[str] = players.split(': ', 1)[1:]

        return player_list if not player_list else player_list[0].split(', ')

    def interrupt_mode(self) -> None:
        while cmd := input():
            print(self.run(cmd))


if __name__ == '__main__':
    with MCRcon() as mr:
        while selector := input("请输入你的选择器: "):
            if test_selector(selector, mr):
                uuids = mr.get_uuid(selector)
                print(f"匹配这个选择器实体的uuid是: {uuids}")
            else:
                print("无效的选择器")
        # player_scoreboards = mr.get_scoreboards(f'Peter_2500')
        # print(player_scoreboards)
        # scoreboard_need = 'kills'
        # print(f'{scoreboard_need}计分板的数值是: {player_scoreboards.get(scoreboard_need)}')
        # print(mr.get_players())
        #
        # mr.interrupt_mode()
