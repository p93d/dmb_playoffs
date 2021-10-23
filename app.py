from flask import Flask, render_template
import flea_flicker_tools
import pandas as pd





"""
format = seed: [team id, league id, team/manager name]
"""
teams = {
    'NFC #1': ['1656657', '326370', 'Patrick Donovan'],
    'NFC #2': ['1656714', '326382', 'Derek Hubbard'],
    'NFC #3': ['1656918', '326384', 'Parker Jackering'],
    'NFC #4': ['1656796', '326387', 'Tyler Stuntebeck'],
    'AFC #1': ['1658135', '326370', 'timmer5500'],
    'AFC #2': ['1666713', '326387', 'bmweber33'],
    'AFC #3': ['1656658', '326375', 'MJahnke'],
    'AFC #4': ['1656921', '326375', 'Trent Davis'],
}


matchups = [
    ['NFC #1', 'NFC #4'],
    ['NFC #2', 'NFC #3'],
    ['AFC #1', 'AFC #4'],
    ['AFC #2', 'AFC #3'],
]



week = 7




app = Flask(__name__)

@app.route("/matchups")
def matchup_info():

    dfs = []
    home_titles = ['n/a']
    away_titles = ['n/a']


    for matchup in matchups:
        # variables for each team id/league/name
        # for easier troubleshooting
        home_team_id = teams[matchup[0]][0]
        home_team_league_id = teams[matchup[0]][1]
        home_team_name = teams[matchup[0]][2]
        home_team_seed = matchup[0]

        away_team_id = teams[matchup[1]][0]
        away_team_league_id = teams[matchup[1]][1]
        away_team_name = teams[matchup[1]][2]
        away_team_seed = matchup[1]


        # get weekly rosters for each team in each matchup
        dfs.append(flea_flicker_tools.create_matchup(
            home_team = [
                home_team_id,
                home_team_league_id,
                home_team_name,
                home_team_seed
            ],
            away_team = [
                away_team_id,
                away_team_league_id,
                away_team_name,
                away_team_seed
            ],
            week=week
        )[0]
        )

        home_titles.append(f"{home_team_name} ({home_team_seed})")
        away_titles.append(f"{away_team_name} ({away_team_seed})")
        


    return render_template('tables.html', tables=dfs, home_titles=home_titles, away_titles=away_titles)


@app.route("/scoreboard")
@app.route("/")
def scores():

    dfs = []
    

    for matchup in matchups:

        # variables for each team id/league/name
        # for easier troubleshooting
        home_team_id = teams[matchup[0]][0]
        home_team_league_id = teams[matchup[0]][1]
        home_team_name = teams[matchup[0]][2]
        home_team_seed = matchup[0]

        away_team_id = teams[matchup[1]][0]
        away_team_league_id = teams[matchup[1]][1]
        away_team_name = teams[matchup[1]][2]
        away_team_seed = matchup[1]


        # get weekly rosters for each team in each matchup
        dfs.append(flea_flicker_tools.create_matchup(
            home_team = [
                home_team_id,
                home_team_league_id,
                home_team_name,
                home_team_seed
            ],
            away_team = [
                away_team_id,
                away_team_league_id,
                away_team_name,
                away_team_seed
            ],
            week=week
        )[1]
        )

    

    return render_template('tables.html',  tables=dfs, home_titles=[], away_titles=[])





if __name__ == "__main__":
    app.run(debug=True)