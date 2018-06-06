import rivercrossingsolver as rcs

game_players = "W1 W2 K1 K2"

rcs.setPlayers(game_players)
rcs.setdrivers(game_players)
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("W1,W2 W1,K1 W2,K1 W1,K2 W2,K2")
rcs.setinvalidBank("")
rcs.setboatCapacity(2)

rcs.solve()
