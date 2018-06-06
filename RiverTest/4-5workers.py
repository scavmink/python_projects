import rivercrossingsolver as rcs

game_players = "1 2 3 4 5"

rcs.setPlayers(game_players)
rcs.setdrivers(game_players)
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("1,2 2,3 3,4 4,5 5,1")
rcs.setinvalidBank("1,2 2,3 3,4 4,5 5,1")
rcs.setboatCapacity(2)

rcs.solve()
