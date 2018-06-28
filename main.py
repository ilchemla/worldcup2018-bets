import os
from operator import itemgetter

from utils import Games
from utils.Bets import Bets
from utils.DingTalk import DingtalkRobot
from config.config import cfg

# Get Match Results
fixtures = Games.get_fixtures()
games_results = []
for ids, game in enumerate(fixtures):
    if game['matchday'] > 3:
        continue

    result = 'X'
    if game['result']['goalsHomeTeam'] > game['result']['goalsAwayTeam']:
        result = '1'

    if game['result']['goalsHomeTeam'] < game['result']['goalsAwayTeam']:
        result = '2'

    if game['status'] != 'FINISHED':
        result = 'TIMED'

    print("Match {} :: {} - {} :: {}".format(ids, game['homeTeamName'], game['awayTeamName'], result))

    if game['status'] != 'FINISHED':
        continue

    games_results.append(result)

print('Current finished game: {}'.format(len(games_results)))

# Get Bets
current_folder = os.path.dirname(os.path.realpath(__file__))
bets_file = os.path.join(current_folder, 'bets.csv')
players_bets = Bets(bets_file).get_all_bets()

# Compute score
## Init score
players_scores = {}
for player in players_bets:
    players_scores[player['employee_username']] = 0


for game_id, game_score in enumerate(games_results):
    for player_id, player in enumerate(players_bets):
        if players_bets[player_id]['bets'][game_id] == game_score:
            players_scores[player['employee_username']] += Games.get_match_weight(game_id)

print players_scores

# Sort results
sorted_results = sorted(players_scores.items(), key=itemgetter(1), reverse=True)

# Print to DingTalk
robot = DingtalkRobot(token=cfg['DINGTALK_TOKEN'])
msg = 'Please find current statistics:\n'
msg += 'Current finished game: {}\n\n'.format(len(games_results))
for score in sorted_results:
    msg += '{}:\t\t{}\n'.format(score[0], score[1])

print(msg)

#robot.send_text(msg)

