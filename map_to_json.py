import json


def create_json(width, height, tileset_id, data):
    return {
        "autoplayBgm": False,
        "autoplayBgs": False,
        "battleback1Name": "",
        "battleback2Name": "",
        "bgm": {
            "name": "",
            "pan": 0,
            "pitch": 100,
            "volume": 90
        },
        "bgs": {
            "name": "",
            "pan": 0,
            "pitch": 100,
            "volume": 90
        },
        "disableDashing": False,
        "displayName": "",
        "encounterList": [],
        "encounterStep": 30,
        "height": height,
        "note": "",
        "parallaxLoopX": False,
        "parallaxLoopY": False,
        "parallaxName": "",
        "parallaxShow": False,
        "parallaxSx": 0,
        "parallaxSy": 0,
        "scrollType": 0,
        "specifyBattleback": False,
        "tilesetId": tileset_id,
        "width": width,
        "data": data,
        "events": []
    }


def create_data(map, width, height):
    data = []
    for r in range(6):
        for y in range(height):
            for x in range(width):
                data.append(map[y][x][r])
    return data


def main(map, tileset_id, map_id):
    (width, height) = (len(map[0]), len(map))
    data = create_data(map, width, height)
    map_json = create_json(width, height, tileset_id, data)

    with open(f'output/Map{map_id:03}.json', 'w') as file:
        json.dump(map_json, file, separators=(',', ':'))
