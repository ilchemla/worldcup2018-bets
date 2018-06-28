import json
import requests

from config.config import cfg


def get_fixtures():
    headers = {'X-Auth-Token': cfg['FOOTBALL']['API_TOKEN'], 'X-Response-Control': 'minified'}
    contents = requests.get(cfg['FOOTBALL']['API_ENDPOINT'], headers=headers)
    contents = json.loads(contents.text)
    return contents['fixtures']


def get_match_weight(match_id):
    weights = [1, 1, 1, 2, 4, 8, 0, 16]
    match_days = [
        range(0, 16),
        range(16, 32),
        range(32, 48),
        range(48, 56),
        range(56, 60),
        range(60, 62),
        [62],
        [63]
    ]

    for day, ids in enumerate(match_days):
        if match_id in ids:
            return weights[day]

    return 0
