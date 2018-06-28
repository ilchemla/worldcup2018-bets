import os

import click

from config.config import cfg
from utils import Games
from utils.Bets import Bets
from utils.DingTalk import DingtalkRobot


@click.command()
@click.option('--dryrun', is_flag=True,
              help='Enables verbose mode.')
def stats(dryrun):
    msg = 'Hello friends, \n' \
          'I took some time to compute some statistics for tonight\'s games\n\n'

    current_folder = os.path.dirname(os.path.realpath(__file__))
    bets_file = os.path.join(current_folder, 'bets.csv')
    player_bets = Bets(bets_file).get_all_bets()

    games_stats = {}
    games_ids = [46, 47]

    fixtures = Games.get_fixtures()

    for game in games_ids:
        games_stats[game] = {
            '1': 0,
            '2': 0,
            'X': 0
        }

    for player in player_bets:
        bets = player['bets']
        for game in games_ids:
            games_stats[game][bets[game]] += 1

    for game in games_ids:
        msg += 'For Match {} :: {} - {} \n'.format(game, fixtures[game]['homeTeamName'], fixtures[game]['awayTeamName'])
        msg += '{} players bet on {} (1)\n'.format(games_stats[game]['1'], fixtures[game]['homeTeamName'])
        msg += '{} players bet on {} (2)\n'.format(games_stats[game]['2'], fixtures[game]['awayTeamName'])
        msg += '{} players bet on Draw (X)\n\n'.format(games_stats[game]['X'])

    msg += 'Good luck...'

    print msg
    robot = DingtalkRobot(token=cfg['DINGTALK_TOKEN'])
    if not dryrun:
        robot.send_text(msg)


if __name__ == '__main__':
    stats()
