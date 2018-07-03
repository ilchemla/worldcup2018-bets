import json
import requests

from config.config import cfg


def get_headers():
    return {'X-Auth-Token': cfg['FOOTBALL']['API_TOKEN'], 'X-Response-Control': 'minified'}


def get_fixtures():
    contents = requests.get(cfg['FOOTBALL']['API_ENDPOINT'], headers=get_headers())
    contents = json.loads(contents.text)
    return contents['fixtures']


def get_fixtures_v2():
    url = cfg['FOOTBALL']['API_ENDPOINT_V2'] + '/competitions/2000/matches'
    contents = requests.get(url, headers=get_headers())
    contents = json.loads(contents.text)
    return contents['matches']


def get_team_flag(team_id):
    response_ = requests.get('http://api.football-data.org/v1/teams/' + str(team_id), headers=get_headers())
    response_ = json.loads(response_.text)
    return response_['crestUrl']


def get_match_weight(match_id):
    weight_per_round = [1, 1, 1, 2, 4, 8, 0, 16]
    match_ids = [
        range(0, 16),
        range(16, 32),
        range(32, 48),
        range(48, 56),
        range(56, 60),
        range(60, 62),
        [62],
        [63]
    ]

    for day, ids in enumerate(match_ids):
        if match_id in ids:
            return weight_per_round[day]

    return 0
