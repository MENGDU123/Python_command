from unittest import case

from rcon.source import Client
import uuid
import json


from config import *


def java_style_json_to_dict(java_json: str) -> dict:
    outer = java_json[0] + java_json[-1]
    new = java_json[1:-1]
    # print(new)


    if outer == "{}":
        result = {}
        stack = []
        seq = ""
        key = ""
        value = ""

        for i in new:
            if i not in [" ", ":", ","] or stack:
                seq += i

            if i == ":" and not stack:
                key = seq
                seq = ""

            elif stack and stack[-1] + i in ["{}", "[]", "()", "\"\""]:
                stack.pop()

                if not stack:
                    result[key] = java_style_json_to_dict(seq)
                    seq = ""

            elif i in ["{", "[", "(", "\""]:

                stack.append(i)

            elif i == "," and not stack:
                if seq:
                    result[key] = seq
                seq = ""
                key = ""

    elif outer == "[]":
        result = []
        stack = []
        seq = ""

        for i in new:
            if i not in [" ", ","] or stack:
                seq += i

            if stack and stack[-1] + i in ["{}", "[]", "()", "\"\""]:
                stack.pop()

                if not stack:
                    result.append(java_style_json_to_dict(seq))
                    seq = ""

            elif i in ["{", "[", "(", "\""]:
                stack.append(i)

            elif i == "," and not stack:
                if seq:
                    result.append(seq)
                seq = ""

    elif outer == "\"\"":
        result = new

    else:
        result = java_json

    return result


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

    def get_data(self, target: str, arg: str) -> dict:
        if target not in ["block", "entity", "storage"]:
            raise Exception(f'Unknown target: {target}')
        response = self.run(f'data get {target} {arg}')
        response = response.split(": ", 1)[1]
        # response = json.loads(response)
        return (response)

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
        uuids = mr.get_uuid("@e[type=pig]")

        for uuid in uuids:
            r = mr.get_data("entity", str(uuid))
            print(r)
            print(json.dumps(java_style_json_to_dict(r), indent=4))

            break

        # while selector := input("请输入你的选择器: "):
            # if test_selector(selector, mr):
            #     uuids = mr.get_uuid(selector)
            #     print(f"匹配这个选择器实体的uuid是: {uuids}")
            # else:
            #     print("无效的选择器")
        # player_scoreboards = mr.get_scoreboards(f'Peter_2500')
        # print(player_scoreboards)
        # scoreboard_need = 'kills'
        # print(f'{scoreboard_need}计分板的数值是: {player_scoreboards.get(scoreboard_need)}')
        # print(mr.get_players())
        #
        # mr.interrupt_mode()
