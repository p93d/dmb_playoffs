from flask import Flask, render_template
import flea_flicker_tools
import pandas as pd





"""
matchups = [
    [home team, away team],
    etc
]
"""
matchups = [
    ['1656657', '1656714'],
    ['1656918', '1656796']
]

owner_to_league = {
    '1656657': '326370',    #Me
    '1656714': '326382',    #DHubb
    '1656918': '326384',    #Parker
    '1656796': '326387',    #Tyler
}

team_list = {
    '1656657': 'PD',
    '1656714': 'DHubb',
    '1656918': 'ParkJack',
    '1656796': 'TylerS',
}





app = Flask(__name__)

@app.route("/tables")
@app.route("/")
def home():

    dfs = []

    for matchup in matchups:

        dfs.append(flea_flicker_tools.create_matchup(
            home_team = [
                matchup[0], owner_to_league[matchup[0]]
            ],
            away_team = [
                matchup[1], owner_to_league[matchup[1]]
            ],
            week = 7
        ).to_html(index=False))#, classes='table table-striped'))
    

    return render_template('tables.html',  tables=dfs, titles=['Matchup #1', 'Matchup #1', "Matchup #2"])





if __name__ == "__main__":
    app.run(debug=True)