# Get Bets
import json
import os

import requests

from utils.Bets import Bets


PLAYER_NAME = ''
MATCH_DAYS = [1, 2, 3]

if __name__ == '__main__':
    current_folder = os.path.dirname(os.path.realpath(__file__))
    bets_file = os.path.join(current_folder, 'bets.csv')
    player_bets = Bets(bets_file).get_player_bets(PLAYER_NAME)

    print player_bets

    contents = requests.get('http://api.football-data.org/v1/competitions/467/fixtures')
    contents = json.loads(contents.text)

    # Print Bets by Match
    print('Current bets status for {}'.format(PLAYER_NAME))
    games_results = []
    for ids, game in enumerate(contents['fixtures']):
        if game['matchday'] not in MATCH_DAYS:
            continue

        result = 'X'
        if game['result']['goalsHomeTeam'] > game['result']['goalsAwayTeam']:
            result = '1'

        if game['result']['goalsHomeTeam'] < game['result']['goalsAwayTeam']:
            result = '2'

        if game['status'] != 'FINISHED':
            result = 'TIMED'

        print(
            "Match {} :: {} - {} :: Your bet: {} :: Result: {}".format(ids, game['homeTeamName'], game['awayTeamName'],
                                                                       player_bets[ids], result))

        if game['status'] != 'FINISHED':
            continue

        games_results.append(result)
