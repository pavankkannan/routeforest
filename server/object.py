import server.data as data
import sqlite3
import json
import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
matplotlib.use('Agg')

from collections import Counter

class Player:
    def __init__(self, name, number, team, position, totYards, totAirYards, totYAC, totReceptions, totTargets, totTDs, routeTree, routePercentages, headshot, college, recsRank, recYardsRank, tdsRank):
        self._Name = name
        self._Number = number
        self._Team = team
        self._Position = position
        self._TotYards = totYards
        self._TotAirYards = totAirYards
        self._TotYAC = totYAC
        self._TotReceptions = totReceptions
        self._TotTargets = totTargets
        self._TotTDs = totTDs
        self._RouteTree = routeTree
        self._RoutePercentages = routePercentages
        self._Headshot = headshot
        self._College = college
        self._RecsRank = recsRank
        self._RecYardsRank = recYardsRank
        self._TDsRank = tdsRank
    @property
    def Name(self):
        return self._Name
    @property
    def Number(self):
        return self._Number
    @property
    def Team(self):
        return self._Team
    @property
    def Position(self):
        return self._Position
    @property
    def TotYards(self):
        return self._TotYards
    @property
    def TotAirYards(self):
        return self._TotAirYards
    @property
    def TotYAC(self):
        return self._TotYAC
    @property
    def TotReceptions(self):
        return self._TotReceptions
    @property
    def TotTargets(self):
        return self._TotTargets
    @property
    def TotTDs(self):
        return self._TotTDs
    @property
    def RouteTree(self):
        return self._RouteTree
    @property
    def RoutePercentages(self):
        return self._RoutePercentages
    @property
    def Headshot(self):
        return self._Headshot
    @property
    def College(self):
        return self._College
    @property
    def RecsRank(self):
        return self._RecsRank
    @property
    def RecYardsRank(self):
        return self._RecYardsRank
    @property
    def TDsRank(self):
        return self._TDsRank
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class Route:
    def __init__(self, preSnap, preCatch, postCatch, routeType):
        self._PreSnap = preSnap
        self._PreCatch = preCatch
        self._PostCatch = postCatch
        self._RouteType = routeType
    @property
    def PreSnap(self): # List of Route point tuples before ball snap
        return self._PreSnap
    @property
    def PreCatch(self): # List of Route point tuples after ball snap before ball caught
        return self._PreCatch
    @property
    def PostCatch(self): # List of Route points after ball caught until end of data
        return self._PostCatch
    @property
    def RouteType(self): # Type of route run - hitch, out, in, etc...
        return self._RouteType

class RoutePoint:
    def __init__(self, xy, event, frame, time):
        self._XY = xy 
        self._Event = event
        self._Frame = frame
        self._Time = time
    @property
    def XY(self): # coordinate tuple (x,y)
        return self._XY
    @property
    def Event(self): # ball snap, ball caught, out of bounds, etc...
        return self._Event
    @property
    def Frame(self): # 1,2,3, etc...
        return self._Frame
    @property
    def Time(self):
        return self._Time
    

def getRoute(dbConn, playerName, playID, tableName): ## given a play name, player id and week number, returns a single route a player ran
    query = f"""
            SELECT x, y, event, frameID, time, playDirection, route
            FROM {tableName}
            WHERE displayName = ? AND playID = ?;
            """
    result = data.select_n_rows(dbConn, query, [playerName, playID])

    rawRoute = []
    routeName = "OTHER"
    for row in result: # Normalizes(?) the points so all plays go the same direction
        y = row[1]

        routeName = row[6]

        if row[5] == "left" and row[0] > 60:
            x = row[0] - 2 * (row[0] - 60)
        elif row[5] == "left" and row[0] < 60:
            x = row[0] + 2 * (60 - row[0])
        else:
            x = row[0]

        # rawRoute.append(RoutePoint((y * (-1), x), row[2], row[3], row[4])) 
        rawRoute.append(RoutePoint((x, y), row[2], row[3], row[4])) 
    splitRoute = [[],[],[]]

    routeSection = 0
    for point in rawRoute:
        if point.Event == "ball_snap":
            routeSection = 1
        elif point.Event == "pass_outcome_caught":
            routeSection = 2
        (splitRoute[routeSection]).append(point)

    route = Route(splitRoute[0], splitRoute[1], splitRoute[2], routeName)
    return route # returns the whole route


def getCatchesByPlayer(dbConn, playerName): #Given a player name, returns a list of routes where they caught the ball, calls getRoute multiple times
    query = """
            SELECT full_name, play_id, pbp.week
            FROM pbp
            JOIN roster2018 ON pbp.receiver_player_id = roster2018.gsis_id
            WHERE full_name = ? AND posteam != "None" AND complete_pass = 1 AND pbp.week <= 17
            ORDER BY pbp.week ASC;
            """
    result = data.select_n_rows(dbConn, query, [playerName])

    catches = []
    for row in result:
        playID = row[1]
        week = row[2]

        route = getRoute(dbConn, playerName, playID, "week" + str(week))
        catches.append(route)

    return catches

def graphRoutes(plays):

    def rotate(x, y):
        return [-y_i for y_i in y], x

    for play in plays:
        (preSnapX, preSnapY) = rotate([cords.XY[0] for cords in play.PreSnap], [cords.XY[1] for cords in play.PreSnap])
        (preCatchX, preCatchY) = rotate([cords.XY[0] for cords in play.PreCatch], [cords.XY[1] for cords in play.PreCatch]) 
        (postCatchX, postCatchY) = rotate([cords.XY[0] for cords in play.PostCatch], [cords.XY[1] for cords in play.PostCatch]) 


        if postCatchX:
            preCatchX.append(postCatchX[0])
            preCatchY.append(postCatchY[0])

        plt.plot(preSnapX, preSnapY, linestyle='dotted',  color='lightblue', linewidth=0.5)
        plt.plot(preCatchX, preCatchY, 'lightblue', linewidth=0.5)
        plt.plot(postCatchX, postCatchY, 'lightcoral', linewidth=0.5)
    
    image = mpimg.imread("server/static/clearField2.png")
    # xydims = [0, 120, 0, 53.3]
    xydims = [-53.3, 0, 0, 120]
    fig = plt.imshow(image, extent=xydims)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig('server/static/annotatedField2.png', bbox_inches='tight', pad_inches = 0, dpi=1200, transparent=True)
    plt.close()

    # print("PreSnapXY: (", preSnapX)

def graphRoutes2(playerName):

    def rotate(x, y):
        return [-y_i for y_i in y], x

    filename = 'server/static/players/' + playerName + '.json'
    with open(filename, 'r') as file:
        player_data = json.load(file)

    plays = player_data.get("routeTree")

    for play in plays:
        (preSnapX, preSnapY) = rotate([cords.xy[0] for cords in play.preSnap], [cords.xy[1] for cords in play.preSnap])
        (preCatchX, preCatchY) = rotate([cords.xy[0] for cords in play.preCatch], [cords.xy[1] for cords in play.preCatch]) 
        (postCatchX, postCatchY) = rotate([cords.xy[0] for cords in play.postCatch], [cords.xy[1] for cords in play.postCatch]) 


        if postCatchX:
            preCatchX.append(postCatchX[0])
            preCatchY.append(postCatchY[0])

        plt.plot(preSnapX, preSnapY, linestyle='dotted',  color='lightblue', linewidth=0.5)
        plt.plot(preCatchX, preCatchY, 'lightblue', linewidth=0.5)
        plt.plot(postCatchX, postCatchY, 'lightcoral', linewidth=0.5)
    
    image = mpimg.imread("server/static/clearField2.png")
    # xydims = [0, 120, 0, 53.3]
    xydims = [-53.3, 0, 0, 120]
    fig = plt.imshow(image, extent=xydims)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig('server/static/annotatedField2.png', bbox_inches='tight', pad_inches = 0, dpi=1200, transparent=True)
    plt.close()



def graphRouteCounts(routeCounts):
    total = sum(routeCounts.values())
    labels = [f'{route}: {count} ({count/total:.1%})' for route, count in routeCounts.items()]

    # plt.pie(routeCounts.values(), labels=labels, textprops={'color': "white"})
    patches, texts = plt.pie(routeCounts.values(), startangle=90)
    plt.legend(patches, labels, loc="center right", bbox_to_anchor=(1.5, 0.5))
    plt.tight_layout()
    plt.savefig('server/static/pie.png', bbox_inches='tight', pad_inches = 0, dpi=1200, transparent=True)
    plt.close()

def getPlayerRanks(playerName):
    with open('server/ranks.json', 'r') as file:
        data = json.load(file)
    return data[playerName]



def getPlayerInfo(playerName): # Returns basic player info, team, jeresey num, receiving yards, etc...
    dbConn = sqlite3.connect('nfl_data.db', check_same_thread=False)
    query = """
            SELECT full_name, roster2018.jersey_number, team, position, sum(receiving_yards), sum(yards_after_catch), sum(complete_pass), count(complete_pass), sum(touchdown), headshot_url, college
            FROM pbp
            JOIN roster2018 ON pbp.receiver_player_id = roster2018.gsis_id
            WHERE full_name = ? AND pbp.week <= 17;
            """
    result = data.select_one_row(dbConn, query, [playerName])

    start = time.time()
    routes = getCatchesByPlayer(dbConn, result[0])
    end = time.time()
    print(f"getCatchesByPlayer: {end - start}")

    dbConn.close()

    routeCounts = Counter(route.RouteType for route in routes)

    ranks = getPlayerRanks(result[0])

    player = Player(result[0], result[1], result[2], result[3], result[4], (result[4]-result[5]), result[5], result[6], result[7], result[8], routes, routeCounts, result[9], result[10], ranks['recs'], ranks['recYards'], ranks['tds'])


    graphRoutes(routes)
    graphRouteCounts(routeCounts)

    return player


def genAllPlayers(): #gets all players who caught a pass during the 2018 season
    dbConn = sqlite3.connect('nfl_data.db', check_same_thread=False)

    query = """
            SELECT full_name, receiver_jersey_number, posteam, headshot_url
            FROM pbp
            JOIN roster2018 ON pbp.receiver_player_id = roster2018.gsis_id
            WHERE complete_pass = 1 AND pbp.week <= 17
            GROUP BY full_name
            ORDER BY last_name ASC, first_name ASC;
            """

    result = data.select_n_rows(dbConn, query)

    players = []
    for row in result:
        players.append({"name": row[0], "jersey": row[1], "team": row[2], "headshot": row[3]})

    dbConn.close()

    with open('server/players.json', 'w') as file:
        json.dump(players, file, indent=4)

    return players

def genRanks():
    dbConn = sqlite3.connect('nfl_data.db', check_same_thread=False)

    query = """
            SELECT full_name,
                RANK () OVER (PARTITION BY roster2018.position ORDER BY sum(complete_pass) DESC) AS recRankPos,
                RANK () OVER (ORDER BY sum(complete_pass) DESC) AS recRankAll,
                RANK () OVER (PARTITION BY roster2018.position ORDER BY sum(receiving_yards) DESC) AS recYardRankPos,
                RANK () OVER (ORDER BY sum(receiving_yards) DESC) AS recYardRankAll,
                RANK () OVER (PARTITION BY roster2018.position ORDER BY sum(touchdown) DESC) AS tdRankPos,
                RANK () OVER (ORDER BY sum(touchdown) DESC) AS tdRankAll
            FROM pbp
            JOIN roster2018 ON pbp.receiver_player_id = roster2018.gsis_id
            WHERE pbp.week <= 17
            GROUP BY receiver_player_id;
            """
    result = data.select_n_rows(dbConn, query)

    ranks = {}
    for row in result:
        playerName = row[0]
        newEntry = {"recs": (row[1], row[2]), "recYards": (row[3], row[4]), "tds": (row[5], row[6])}
        ranks[playerName] = newEntry

    dbConn.close()

    with open('server/ranks.json', 'w') as file:
        json.dump(ranks, file, indent=4)

    return ranks

def createPlayerJson(playerName):
    filename = playerName.replace(" ", "_") + ".json"
    try:
        with open(filename, 'w') as json_file:
            jsonString = getPlayerInfo(playerName).toJSON()
            json_file.write(jsonString)
        print(f"Object successfully saved to {filename}")
    except Exception as error:
        print(f"Failed to save object to JSON file: {error}")