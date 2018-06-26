import click
import csv

from utils.DingTalk import DingtalkRobot
from config.config import cfg


def get_bets():
    # Get Bets
    players_bets = []
    with open('bets.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for idx, row in enumerate(spamreader):
            if idx == 0:
                continue

            row = row[0].split(',')
            employee_id = row[0]
            employee_username = row[1]
            player_bets = row[2:]
            players_bets.append({
                'employee_id': employee_id,
                'employee_username': employee_username,
                'bets': player_bets
            })

    return players_bets


def get_who_to_remind(players_bets):
    to_remind = []
    for player in players_bets:
        size = len(player['bets'])
        if size != 48:
            to_remind.append(player['employee_username'])

    print('Players to remind: {}'.format(to_remind))
    return to_remind


@click.command()
@click.option('--dryrun', is_flag=True,
              help='Enables verbose mode.')
def remind(dryrun):
    players_bets = get_bets()
    to_remind = get_who_to_remind(players_bets)

    msg = ''
    for user in to_remind:
        msg += '@' + user + '\n'

    msg += 'You have less than 30minutes to send your bets for Round 3!'

    robot = DingtalkRobot(token=cfg['DINGTALK_TOKEN'])
    if not dryrun:
        robot.send_text(msg)


if __name__ == '__main__':
    remind()
