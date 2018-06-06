import rivercrossingsolver as rcs
from itertools import combinations

game_players = "P F M D S"

rcs.setPlayers(game_players)
rcs.setdrivers(game_players)
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.settimeLimit(30)
rcs.settimeValues("P:1 F:3 M:6 D:8 S:12")
rcs.setduplicateNode(True)

rcs.solve("train")
