import datetime
from string import Template

import click

from config.config import cfg
from utils import Games


@click.command()
@click.option('--match-day', required=True, help='Round\'s number', type=int)
def generate_gui(match_day):
    print('Generating bets table for round {}...'.format(match_day))

    # Get fixtures
    fixtures = Games.get_fixtures_v2()
    games_divs = []
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    for ids, game in enumerate(fixtures):
        if game['stage'] != 'QUARTER_FINALS':
            continue

        date_obj = datetime.datetime.strptime(game['utcDate'], date_format)
        date_obj += datetime.timedelta(hours=3)

        homeTeamFlag = '<img src={} width=32/>'.format(Games.get_team_flag(game['homeTeam']['id']))
        awayTeamFlag = '<img src={} width=32/>'.format(Games.get_team_flag(game['awayTeam']['id']))

        div = '<tr>'
        div += "<td>Match {}</td><td>{} {} - {} {}</td>".format(ids, homeTeamFlag, game['homeTeam']['name'], game['awayTeam']['name'], awayTeamFlag)
        div += "<td>{}</td>".format(date_obj.strftime('%d %b %Y %H:%M %Z%z'))
        div += '<td>'
        div += '<select name="games[{}]" class="form-control" required>'
        div += '<option selected value> -- select your bet -- </option>'
        div += '<option value="1">{} wins (1)</option>'.format(game['homeTeam']['name'])
        div += '<option value="2">{} wins (2)</option>'.format(game['awayTeam']['name'])
        div += '<option value="X">Draw (X)</option>'
        div += '</select>'
        div += '</td>'
        div += '</tr>'
        games_divs.append(div)

    # open the file
    filein = open('bets_template.html')
    # read it
    src = Template(filein.read())
    # document data
    d = {
        'games': ''.join(games_divs),
        'matchDay': match_day,
        'fcurl': cfg['FC_URL']
    }
    # do the substitution
    result = src.substitute(d)

    output_file = "dist/bets_{}.html".format(match_day)
    file = open(output_file, "w")
    file.write(result)
    file.close()
    print('Done. Output path: {}'.format(output_file))


if __name__ == '__main__':
    generate_gui()