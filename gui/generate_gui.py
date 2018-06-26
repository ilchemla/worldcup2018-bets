import datetime
from string import Template

import pytz
import requests
import json

# Get Match
contents = requests.get('http://api.football-data.org/v1/competitions/467/fixtures')
contents = json.loads(contents.text)

# Match Day
match_day = 3

# Get Match Results
games_divs = []
date_format = "%Y-%m-%dT%H:%M:%SZ"
for ids, game in enumerate(contents['fixtures']):
    if game['matchday'] != match_day:
        continue

    date_obj = datetime.datetime.strptime(game['date'], date_format)
    date_obj += datetime.timedelta(hours=3)

    div = '<tr>'
    div += "<td>Match {}</td><td>{} - {}</td>".format(ids, game['homeTeamName'], game['awayTeamName'])
    div += "<td>{}</td>".format(date_obj.strftime('%d %b %Y %H:%M %Z%z'))
    div += '<td>'
    div += '<select name="games[{}]" class="form-control" required>'
    div += '<option selected value> -- select your bet -- </option>'
    div += '<option value="1">{} wins (1)</option>'.format(game['homeTeamName'])
    div += '<option value="2">{} wins (2)</option>'.format(game['awayTeamName'])
    div += '<option value="X">Draw (X)</option>'
    div += '</select>'
    div += '</td>'
    #div += '<td><input type="text" name="games[{}]" placeholder="your bet for game_{}"></td>'.format(ids,ids)
    div += '</tr>'
    games_divs.append(div)

#open the file
filein = open('bets_template.html')
#read it
src = Template(filein.read())
#document data
games = "This is the title"
d={ 'games': ''.join(games_divs), 'matchDay': match_day}
#do the substitution
result = src.substitute(d)

file = open("dist/bets_{}.html".format(match_day), "w")
file.write(result)
file.close()