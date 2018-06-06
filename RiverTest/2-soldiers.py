import rivercrossingsolver as rcs

game_players = "A L B1 B2"

rcs.setPlayers(game_players)
rcs.setdrivers(game_players)
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("L A,L A,B1 A,B2")
rcs.setinvalidBank("L")
rcs.setboatCapacity(2)

rcs.solve("soldiers")
