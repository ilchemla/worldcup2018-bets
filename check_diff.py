from utils import Games

fixtures = Games.get_fixtures()
fixtures_v2 = Games.get_fixtures_v2()

for ids, game in enumerate(fixtures):
    #if game['homeTeamName'] != fixtures_v2[ids]['homeTeam']['name']:
    #    raise Exception('My error! {} {}'.format(game['homeTeamName'], fixtures_v2[ids]['homeTeam']['name']))
    print('{} {} {}'.format(ids, game['homeTeamName'], fixtures_v2[ids]['homeTeam']['name']))