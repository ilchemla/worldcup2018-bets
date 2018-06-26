import csv

from utils.DingTalk import DingtalkRobot
from config.config import cfg

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

to_remind = []
for player in players_bets:
    size = len(player['bets'])
    if size != 48:
        to_remind.append(player['employee_username'])

print(to_remind)

msg = ''
for user in to_remind:
    msg += '@' + user + '\n'

msg += 'You have less than 30minutes to send your bets for Round 3!'

robot = DingtalkRobot(token=cfg['DINGTALK_TOKEN'])
#robot.send_text(msg)
