import datetime
from string import Template

import click
import requests
import json

from config.config import cfg


def get_flag_url(team_link):
    response_ = requests.get(team_link)
    response_ = json.loads(response_.text)
    return response_['crestUrl']


@click.command()
@click.option('--match-day', required=True, help='Round\'s number', type=int)
def generate_gui(match_day):
    print('Generating bets table for round {}...'.format(match_day))
    # Get fixtures
    contents = requests.get('http://api.football-data.org/v1/competitions/467/fixtures')
    contents = json.loads(contents.text)

    games_divs = []
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    for ids, game in enumerate(contents['fixtures']):
        if game['matchday'] != match_day:
            continue

        date_obj = datetime.datetime.strptime(game['date'], date_format)
        date_obj += datetime.timedelta(hours=3)

        homeTeamFlag = '<img src={} width=32/>'.format(get_flag_url(game['_links']['homeTeam']['href']))
        awayTeamFlag = '<img src={} width=32/>'.format(get_flag_url(game['_links']['awayTeam']['href']))

        div = '<tr>'
        div += "<td>Match {}</td><td>{} {} - {} {}</td>".format(ids, homeTeamFlag, game['homeTeamName'], game['awayTeamName'], awayTeamFlag)
        div += "<td>{}</td>".format(date_obj.strftime('%d %b %Y %H:%M %Z%z'))
        div += '<td>'
        div += '<select name="games[{}]" class="form-control" required>'
        div += '<option selected value> -- select your bet -- </option>'
        div += '<option value="1">{} wins (1)</option>'.format(game['homeTeamName'])
        div += '<option value="2">{} wins (2)</option>'.format(game['awayTeamName'])
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

    output_file = "dist/bets_{}.html"
    file = open(output_file.format(match_day), "w")
    file.write(result)
    file.close()
    print('Done. Output path: {}'.format(output_file))


if __name__ == '__main__':
    generate_gui()