import requests
import json
import pandas as pd
import numpy as np



base_url = "https://www.fleaflicker.com/api/"


def get_roster(league_id, team_id, week):

    url = base_url + f"FetchRoster?league_id={league_id}&team_id={team_id}&scoring_period={week}"
    r = requests.get(url)
    results = json.loads(r.text)

    roster = {
        'Slot': [],
        'Player': [],
        'Projected': [],
        'Actual': []
    }

    # go through each starter
    for starter in results['groups'][0]['slots']:

        # get the slot name
        if starter['position']['label'] == "RB/WR/TE":
            roster['Slot'].append('Flx')
        elif starter['position']['label'] == "D/ST":
            roster['Slot'].append('DST')
        else:
            roster['Slot'].append(starter['position']['label'])

        # get player name
        roster['Player'].append(
            starter['leaguePlayer']['proPlayer']['nameFull']
            )

        # if available, get projected points
        try:
            roster['Projected'].append(
                starter['leaguePlayer']['viewingProjectedPoints']['value']
            )
        except:
            roster['Projected'].append('--')

        # if available, get actual points
        try:
            roster['Actual'].append(
                starter['leaguePlayer']['viewingActualPoints']['value']
            )
        except:
            roster['Actual'].append('--')

    proj_pts = 0
    actual_pts = 0

    for proj, actual in zip(roster['Projected'], roster['Actual']):

        if actual == '--':
            if proj == '--':
                continue
            else:
                proj_pts+=proj
        else:
            proj_pts+=actual
            actual_pts+=actual


    roster['Slot'].append('TOTAL')
    roster['Player'].append('')
    roster['Projected'].append(proj_pts)
    roster['Actual'].append(actual_pts)

    # then get Bench info
    for starter in results['groups'][1]['slots']:

        roster['Slot'].append('be')

        # get player name
        roster['Player'].append(
            starter['leaguePlayer']['proPlayer']['nameFull']
            )

        # if available, get projected points
        try:
            roster['Projected'].append(
                starter['leaguePlayer']['viewingProjectedPoints']['value']
            )
        except:
            roster['Projected'].append('--')

        # if available, get actual points
        try:
            roster['Actual'].append(
                starter['leaguePlayer']['viewingActualPoints']['value']
            )
        except:
            roster['Actual'].append('--')


    return roster


# create the matchup table
def create_matchup(home_team, away_team, week):

    # get current roster for given week for both teams
    home_roster = get_roster(home_team[1], home_team[0], week)
    away_roster = get_roster(away_team[1], away_team[0], week)

    boxscore = {
        'Home_Player': home_roster['Player'],
        'Home_Projected': home_roster['Projected'],
        'Home_Actual': home_roster['Actual'],
        'Slot': home_roster['Slot'],
        'Away_Actual': away_roster['Actual'],
        'Away_Projected': away_roster['Projected'],
        'Away_Player': away_roster['Player'],
    }

    df = pd.DataFrame.from_dict(boxscore)

    df.rename(
        columns={
        'Home_Player':'Player',
        'Home_Projected': 'Proj',
        'Home_Actual': 'Actual',
        'Away_Actual': 'Actual',
        'Away_Projected': 'Proj',
        'Away_Player': 'Player',
        },
        inplace=True
    )

    return df