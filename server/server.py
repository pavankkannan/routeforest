from flask import Flask, send_from_directory
import server.object as object
from decouple import config

import json

# source venv/bin/activate

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

