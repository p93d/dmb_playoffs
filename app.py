from flask import Flask, render_template
import flea_flicker_tools
import pandas as pd





"""
format = seed: [team id, league id, team/manager name]
"""
teams = {
'AFC #1': ['1656918', '326384', 'ParkerJackering'],
'AFC #2': ['1656728', '326386', 'Kendall1'],
'NFC #1': ['1656660', '326382', 'TCarl'],
'AFC #3': ['1657203', '326385', 'HilaryBartsch'],
'NFC #2': ['1662084', '326383', 'Rkuhl'],
'AFC #4': ['1656713', '326387', 'NikWerner22'],
'NFC #5': ['1656673', '326382', 'jdavidson27'],
'NFC #3': ['1656765', '326375', 'TAmes'],
'NFC #6': ['1666115', '326383', 'BrandonElliott'],
'AFC #5': ['1656675', '326386', 'Jake Smith'],
'AFC #6': ['1657013', '326384', 'RyanBudden34'],
'NFC #7': ['1657682', '326375', 'Brett Hubbard'],
'NFC #4': ['1656657', '326370', 'Patrick Donovan'],
'NFC #8': ['1661105', '326375', 'ToddBresee'],
'AFC #7': ['1657612', '326384', 'Mattcaley'],
'NFC #9': ['1658135', '326370', 'timmer5500'],
'NFC #10': ['1663035', '326375', 'EliHump'],
'AFC #8': ['1656996', '326387', 'coleneedham00'],
'AFC #9': ['1657314', '326385', 'Brian Cacic'],
'AFC #10': ['1657373', '326387', 'Kevin McGee'],
'AFC #11': ['1656848', '326384', 'marcchiefari'],
'NFC #11': ['1656569', '326370', 'Chad Burkholder'],
'NFC #12': ['1656774', '326382', 'Chad Olmstead'],
'AFC #12': ['1656729', '326385', 'Hingtgen314'],
'NFC #13': ['1656666', '326375', 'ChrisBausch'],
'NFC #14': ['1656714', '326382', 'Derek Hubbard'],
'NFC #15': ['1656658', '326375', 'MJahnke'],
'AFC #13': ['1656701', '326386', 'Devon Calvert'],
'NFC #16': ['1666038', '326375', 'KyleBredeson'],
'AFC #14': ['1656958', '326385', 'NateGraney'],
'AFC #15': ['1657029', '326385', 'KeithMoore'],
'AFC #16': ['1658653', '326384', 'F Chet Pancakes'],
}


matchups = [
    ['NFC #8',  'NFC #16'],
    ['NFC #5', 'NFC #13'],
    ['NFC #6', 'NFC #14'],
    ['NFC #7', 'NFC #15'],
    ['AFC #8',  'AFC #16'],
    ['AFC #12', 'AFC #5'],
    ['AFC #11', 'AFC #6'],
    ['AFC #7', 'AFC #15'],
]


week = 13




app = Flask(__name__)


@app.route("/home")
def home():

    return "Hello World"



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
        matchup_rosters = flea_flicker_tools.create_matchup(
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

        matchup_rosters.rename(
        columns={
        'Home_Player': home_team_name,
        'Away_Player':away_team_name,
        },
        inplace=True
        )

        dfs.append(
            matchup_rosters.to_html(index=False)
        )

        """
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
        """

    # return render_template('boxscores.html', tables=dfs, home_titles=home_titles, away_titles=away_titles)
    return render_template('boxscores.html', tables=dfs, home_titles=[], away_titles=[])


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
