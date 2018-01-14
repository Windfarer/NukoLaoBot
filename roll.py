import random
import re
import requests
import os

RANDOM_API_KEY = os.getenv('RANDOM_API_KEY')
if RANDOM_API_KEY:
    print('random.org api enabled')

dice_pattern = re.compile(r'''([+-]{0,1}(\d+)[Dd](\d+))|([+-]{0,1}(\d+))''')

def get_randint_by_api(max):
    resp = requests.post("https://api.random.org/json-rpc/1/invoke", json={
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            'apiKey': RANDOM_API_KEY,
            'n': 1,
            'min': 1,
            'max': max
        },
        "id": 1
    })
    resp.raise_for_status()
    print(resp.json())
    return resp.json()['result']['random']['data'][0]


def get_randint(max):
    if not RANDOM_API_KEY:
        result = random.randint(1, max)
        print('random local', result)
        return result
    try:
        result = get_randint_by_api(max)
        print('random online', result)
    except Exception as e:
        print(e)
        result = random.randint(1, max)
        print('online failed, random local', result)
    return result

def roll(text, limit=1000):
    groups = dice_pattern.findall(text)
    if len(groups) > limit:
        return []
    result = []
    for group in groups:
        sub_result = []
        if group[0]:
            if group[0].startswith('-'):
                sign = -1
            else:
                sign = 1
            for _ in range(int(group[1])):
                n = int(group[2])
                if n > limit:
                    return []
                sub_result.append(sign * get_randint(n))
        elif group[3]:
            sub_result.append(int(group[3]))
        result.append(sub_result)
    return result