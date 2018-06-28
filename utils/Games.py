import json
import requests

from config.config import cfg


def get_fixtures():
    headers = {'X-Auth-Token': cfg['FOOTBALL']['API_TOKEN'], 'X-Response-Control': 'minified'}
    contents = requests.get(cfg['FOOTBALL']['API_ENDPOINT'], headers=headers)
    contents = json.loads(contents.text)
    return contents['fixtures']
