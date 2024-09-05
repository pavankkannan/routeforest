import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import object

dbConn = sqlite3.connect('nfl_data.db')
dbCursor = dbConn.cursor()

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


# preCatch = ([], [])
# yac = ([],[])

# plays = object.getPlays(dbConn, 2018090600)
# drive1 = plays[8]

# player = object.getPlayerInfo("Allen Robinson")

# object.genAllPlayers()
# object.genRanks()
# ranks = object.getPlayerRanks("Julio Jones")
# print(ranks['recYards'])

# player = object.getPlayerInfo("Larry Fitzgerald")
player = object.createPlayerJson("Rob Gronkowski")
# print(player.RoutePercentages)


# plays = object.getCatchesByPlayer(dbConn, "Stefon Diggs")

# print(object.getAllPlayers(dbConn))

# for play in plays:
#     (preSnapX, preSnapY) = ([cords.XY[0] for cords in play.PreSnap], [cords.XY[1] for cords in play.PreSnap])
#     (preCatchX, preCatchY) = ([cords.XY[0] for cords in play.PreCatch], [cords.XY[1] for cords in play.PreCatch]) 
#     (postCatchX, postCatchY) = ([cords.XY[0] for cords in play.PostCatch], [cords.XY[1] for cords in play.PostCatch]) 
    
#     if postCatchX:
#         preCatchX.append(postCatchX[0])
#         preCatchY.append(postCatchY[0])
    
#     plt.plot(preSnapX, preSnapY, linestyle='dotted',  color='blue', linewidth=0.5)
#     plt.plot(preCatchX, preCatchY, 'blue', linewidth=0.5)
#     plt.plot(postCatchX, postCatchY, 'red', linewidth=0.5)

    
# image = mpimg.imread("field2.png")
# xydims = [0, 120, 0, 53.3]
# fig = plt.imshow(image, extent=xydims)
# plt.axis('off')
# fig.axes.get_xaxis().set_visible(False)
# fig.axes.get_yaxis().set_visible(False)
# plt.savefig('annotatedField.png', bbox_inches='tight', pad_inches = 0, dpi=1200, transparent=True)
# plt.show()





