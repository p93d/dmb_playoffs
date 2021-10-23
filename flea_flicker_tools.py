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

    yet_to_play = 0

    # go through each starter
    for starter in results['groups'][0]['slots']:

        # get the slot name
        if starter['position']['label'] == "RB/WR/TE":
            roster['Slot'].append('Flex')
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
                round(starter['leaguePlayer']['viewingProjectedPoints']['value'], 2)
            )
        except:
            roster['Projected'].append('--')

        # if available, get actual points
        try:
            roster['Actual'].append(
                round(starter['leaguePlayer']['viewingActualPoints']['value'], 2)
            )
        except:
            roster['Actual'].append('--')
            yet_to_play+=1

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
                round(starter['leaguePlayer']['viewingProjectedPoints']['value'], 2)
            )
        except:
            roster['Projected'].append('--')

        # if available, get actual points
        try:
            roster['Actual'].append(
                round(starter['leaguePlayer']['viewingActualPoints']['value'], 2)
            )
        except:
            roster['Actual'].append('--')


    return roster, proj_pts, actual_pts, yet_to_play


# create the matchup table
def create_matchup(home_team, away_team, week):

    # get current roster for given week for both teams
    home_roster, home_proj, home_act, home_yet = get_roster(home_team[1], home_team[0], week)
    away_roster, away_proj, away_act, away_yet = get_roster(away_team[1], away_team[0], week)

    boxscore = {
        'Home_Player': home_roster['Player'],
        'Home_Projected': home_roster['Projected'],
        'Home_Actual': home_roster['Actual'],
        'Slot': home_roster['Slot'],
        'Away_Actual': away_roster['Actual'],
        'Away_Projected': away_roster['Projected'],
        'Away_Player': away_roster['Player'],
    }

    boxscore_df = pd.DataFrame.from_dict(boxscore)

    boxscore_df.rename(
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

    scoreboard_df = pd.DataFrame.from_dict(
        {'Manager': [
            f"{home_team[2]} ({home_team[3]})",
            f"{away_team[2]} ({away_team[3]})",
        ],
        'Yet to Play': [
            home_yet,
            away_yet
        ],
        'Score': [
            home_act,
            away_act
        ],
        'Projected Total': [
            home_proj,
            away_proj
        ]
        }
    )

    return boxscore_df.to_html(index=False), scoreboard_df.to_html(index=False)