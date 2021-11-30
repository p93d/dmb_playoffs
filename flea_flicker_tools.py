import requests
import json
import pandas as pd
import numpy as np



base_url = "https://www.fleaflicker.com/api/"


def game_start_time(unix_timestamp):

    # convert time stamp value to integer, and then subtract
    # six hours (converts to Central time zone)
    full_time = int(unix_timestamp) - (6 * 60 * 60 * 1000)

    # trim off the milliseconds value since we don't need/care
    minus_milli = int(str(full_time)[:-3])

    # return in desired Day HH:MM format
    return datetime.utcfromtimestamp(minus_milli).strftime('%a %I:%M')


"""
Returns the status of the game, and a 0/1
value indicating whether the player has yet to play
"""
def game_status(game_json):

    """
    Determine if:
        1. Player is on BYE
        2. Game has ended
        3. Game is in progress
            a. current score
        4. Game is in the future
    """

        # check for BYE
    if game_json.get('isBye') == True:
        return 'BYE', 0

    # Smaller subset of game data
    game_dict = game_json['game']



    # Determine the score of the game
    away_score = game_dict.get('awayScore', 0)
    home_score = game_dict.get('homeScore', 0)

    if game_json.get('participant') == 'HOME':
        game_score = f'{home_score}-{away_score}'
    else:
        game_score = f'{away_score}-{home_score}'


    # Check if the game is Complete, in-progress,
    # or in the future
    if game_dict.get('status') == 'FINAL_SCORE':
        return f"{game_score}  Final", 0

    elif game_dict.get('status') == 'IN_PROGRESS':
        return f"{game_score}  Q{game_dict.get('segment')}", 0
    else:
        return game_start_time(
            game_dict.get('startTimeEpochMilli')
        ), 1




def get_roster(league_id, team_id, week):

    url = base_url + f"FetchRoster?league_id={league_id}&team_id={team_id}&scoring_period={week}"
    r = requests.get(url)
    results = json.loads(r.text)

    roster = {
        'Slot': [],
        'Player': [],
        'Game_Status': [],
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
        if 'leaguePlayer' in starter:
            roster['Player'].append(
                starter['leaguePlayer']['proPlayer']['nameFull']
                )


            # if available, get projected points
            if 'viewingProjectedPoints' in starter['leaguePlayer']:
                roster['Projected'].append(
                round(starter['leaguePlayer']['viewingProjectedPoints'].get('value'), 2)
                )
            else:
                roster['Projected'].append('--')

            # if available, get actual points
            if 'viewingActualPoints' in starter['leaguePlayer']:
                pts = starter['leaguePlayer']['viewingActualPoints'].get('value', 0)
                roster['Actual'].append(
                    round(pts, 2)
                )
            else:
                roster['Actual'].append('--')

            # Get game status and determine how many players
            # are yet to play
            status_of_game, ytp = game_status(
                starter['leaguePlayer']['requestedGames'][0]
            )
            roster['Game_Status'].append(status_of_game)
            yet_to_play+=ytp

            
        else:
            roster['Player'].append('  ')
            roster['Projected'].append('--')
            roster['Actual'].append('--')
            roster['Game_Status'].append('  ')



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
        if 'leaguePlayer' in starter:
            roster['Player'].append(
                starter['leaguePlayer']['proPlayer']['nameFull']
                )


            # if available, get projected points
            if 'viewingProjectedPoints' in starter['leaguePlayer']:
                roster['Projected'].append(
                round(starter['leaguePlayer']['viewingProjectedPoints'].get('value'), 2)
                )
            else:
                roster['Projected'].append('--')

            # if available, get actual points
            if 'viewingActualPoints' in starter['leaguePlayer']:
                pts = starter['leaguePlayer']['viewingActualPoints'].get('value', 0)
                roster['Actual'].append(
                round(pts, 2)
                )
            else:
                roster['Actual'].append('--')

            # Get game status and determine how many players
            # are yet to play
            status_of_game, ytp = game_status(
                starter['leaguePlayer']['requestedGames'][0]
            )
            roster['Game_Status'].append(status_of_game)

            
        else:
            roster['Player'].append('  ')
            roster['Projected'].append('--')
            roster['Actual'].append('--')
            roster['Game_Status'].append('  ')



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
    
    # Make sure rosters are the same size
    if len(boxscore['Home_Player']) > len(boxscore['Away_Player']):

        for i in range(len(boxscore['Home_Player']) - len(boxscore['Away_Player'])):

            boxscore['Slot'].append('be')
            boxscore['Away_Actual'].append('--')
            boxscore['Away_Projected'].append('--')
            boxscore['Away_Player'].append('--')

    
    if len(boxscore['Away_Player']) > len(boxscore['Home_Player']):

        for i in range(len(boxscore['Away_Player']) - len(boxscore['Home_Player'])):

            boxscore['Slot'].append('be')
            boxscore['Home_Actual'].append('--')
            boxscore['Home_Projected'].append('--')
            boxscore['Home_Player'].append('--')
    

    boxscore_df = pd.DataFrame.from_dict(boxscore)

    boxscore_df.rename(
        columns={
        'Home_Player':'Player',
        'Home_Projected': 'Proj',
        'Home_Actual': 'Score',
        'Away_Actual': 'Score',
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
