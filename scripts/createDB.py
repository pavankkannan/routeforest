import sqlite3
import pandas as pd

dbConn = sqlite3.connect('nfl_data.db', check_same_thread=False)
dbCursor = dbConn.cursor()

roster = pd.read_csv('server/nfl-big-data-bowl-2021/roster_2018.csv', low_memory = False)
roster.to_sql('roster2018', dbConn, if_exists='replace', index = False)

pbp = pd.read_csv('server/nfl-big-data-bowl-2021/pbp2018.csv', low_memory = False)
pbp.to_sql('pbp', dbConn, if_exists='replace', index = False)

games = pd.read_csv('server/nfl-big-data-bowl-2021/games.csv', low_memory = False)
games.to_sql('games', dbConn, if_exists='replace', index = False)

players = pd.read_csv('server/nfl-big-data-bowl-2021/players.csv', low_memory = False)
players.to_sql('players', dbConn, if_exists='replace', index = False)

plays = pd.read_csv('server/nfl-big-data-bowl-2021/plays.csv', low_memory = False)
plays.to_sql('plays', dbConn, if_exists='replace', index = False)

i = 1
while i < 18:
    file = "week" + str(i)
    fileName = "server/nfl-big-data-bowl-2021/" + file + ".csv"
    week = pd.read_csv(fileName, low_memory = False).query("position == 'WR' or position == 'RB' or position == 'FB' or position == 'TE' or position == 'QB'")
    week.to_sql(file, dbConn, if_exists='replace', index = False)
    i += 1