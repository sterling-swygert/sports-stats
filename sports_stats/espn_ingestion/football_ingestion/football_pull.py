import requests
import pandas as pd
import pyarrow as pa
from string import Template


from sports_stats.utils.util import get_project_root


teams_endpoint = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams'

teams_season_endpoint = Template('https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/$year/teams/')

res = requests.request('POST', teams_endpoint)

teams = []
for item in res.json().get('sports')[0].get('leagues')[0].get('teams'):
    team = item.get('team')
    if type(team) == dict:
        teams.append({
            'id': int(team.get('id')),
            'slug': team.get('slug'),
            'name': team.get('name')
        })





