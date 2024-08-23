from flask import Flask, abort, send_from_directory
import server.object as object
from decouple import config

import sqlite3
import pandas as pd
import json

# source venv/bin/activate

# dbConn = sqlite3.connect('nfl_data.db', check_same_thread=False)
# dbCursor = dbConn.cursor()

# roster = pd.read_csv('nfl-big-data-bowl-2021/roster_2018.csv', low_memory = False)
# roster.to_sql('roster2018', dbConn, if_exists='replace', index = False)

# pbp = pd.read_csv('nfl-big-data-bowl-2021/pbp2018.csv', low_memory = False)
# pbp.to_sql('pbp', dbConn, if_exists='replace', index = False)

# games = pd.read_csv('nfl-big-data-bowl-2021/games.csv', low_memory = False)
# games.to_sql('games', dbConn, if_exists='replace', index = False)

# players = pd.read_csv('nfl-big-data-bowl-2021/players.csv', low_memory = False)
# players.to_sql('players', dbConn, if_exists='replace', index = False)

# plays = pd.read_csv('nfl-big-data-bowl-2021/plays.csv', low_memory = False)
# plays.to_sql('plays', dbConn, if_exists='replace', index = False)

# i = 1
# while i < 18:
#     file = "week" + str(i)
#     fileName = "nfl-big-data-bowl-2021/" + file + ".csv"
#     week = pd.read_csv(fileName, low_memory = False)
#     week.to_sql(file, dbConn, if_exists='replace', index = False)
#     i += 1

app = Flask(__name__)

# allPlayers = object.getAllPlayers()

@app.route('/players')
def players():
    with open('server/players.json', 'r') as file:
        data = json.load(file)
    return data

@app.route('/players/<player_name>')
def get_object(player_name):
    playerName = player_name.replace("-", " ")
    try:
        player = object.getPlayerInfo(playerName)
        return {
            "name": player.Name,
            "number": int(player.Number),
            "team": player.Team,
            "position": player.Position,
            "totYards": player.TotYards,
            "totAirYards":player.TotAirYards,
            "totYAC": player.TotYAC,
            "totReceptions": player.TotReceptions,
            "totTargets": player.TotTargets,
            "totTDs": player.TotTDs,
            "routePercentages": player.RoutePercentages,
            "headshot": player.Headshot,
            "college": player.College,
            "recsRank": player.RecsRank, #tuple (positiional rank, overall rank)
            "recYardsRank": player.RecYardsRank, #tuple (positiional rank, overall rank)
            "tdsRank": player.TDsRank, #tuple (positiional rank, overall rank)
        }
    except Exception as e:
        print(e)
        raise e

@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('server/static', filename)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(config("PORT")), debug=True)

