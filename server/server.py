from flask import Flask, send_from_directory
from flask_cors import CORS
import server.object as object
from decouple import config

import json

# source venv/bin/activate
# gunicorn --bind 0.0.0.0:8000 server.server:app
# start server (IN ROOT FOLDER):
# flask --app server.server:app run --host 0.0.0.0 --port 8000

# Initialize Flask app and enable CORS.
app = Flask(__name__)
allow_list = ["http://localhost:3000", "https://pavankkannan.github.io"]
cors = CORS(app, resource={"/*": {"origins": allow_list}})

# allPlayers = object.getAllPlayers()

@app.route('/players')
def players():
    with open('server/players.json', 'r') as file:
        data = json.load(file)
    return data

@app.route('/players/<player_name>')
def get_object(player_name):
    try:
        # player = object.getPlayerInfo(playerName)
        object.graphRoutes2(player_name)
        return '', 204
        #return {
            # "name": player.Name,
            # "number": int(player.Number),
            # "team": player.Team,
            # "position": player.Position,
            # "totYards": player.TotYards,
            # "totAirYards":player.TotAirYards,
            # "totYAC": player.TotYAC,
            # "totReceptions": player.TotReceptions,
            # "totTargets": player.TotTargets,
            # "totTDs": player.TotTDs,
            # "routePercentages": player.RoutePercentages,
            # "headshot": player.Headshot,
            # "college": player.College,
            # "recsRank": player.RecsRank, #tuple (positiional rank, overall rank)
            # "recYardsRank": player.RecYardsRank, #tuple (positiional rank, overall rank)
            # "tdsRank": player.TDsRank, #tuple (positiional rank, overall rank)
        # }
    except Exception as e:
        print(e)
        raise e

@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('server/static', filename)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(config("PORT")), debug=True)

