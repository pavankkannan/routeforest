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

@app.route('/players/fieldView/<player_name>')
def get_fieldView(player_name):
    try:
        # player = object.getPlayerInfo(playerName)
        object.graphRoutes2(player_name)
        return send_from_directory('static/fieldViews', f'{player_name}_FV.png')
    
    except Exception as e:
        print(e)
        raise e

@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('server/static', filename)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(config("PORT")), debug=True)

