import csv


class Bets:
    def __init__(self, csv_path):
        self.csvPath = csv_path
        self.players_bets = []
        self.fetch()

    def fetch(self):
        with open(self.csvPath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for idx, row in enumerate(spamreader):
                if idx == 0:
                    continue

                row = row[0].split(',')
                employee_id = row[0]
                employee_username = row[1]
                player_bets = row[2:]
                self.players_bets.append({
                    'employee_id': employee_id,
                    'employee_username': employee_username,
                    'bets': player_bets
                })

    def get_all_bets(self):
        return self.players_bets

    def get_player_bets(self, player_name):
        for item in self.players_bets:
            if item['employee_username'] == player_name:
                return item['bets']
