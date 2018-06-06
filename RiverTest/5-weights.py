import rivercrossingsolver as rcs

# Father    = 90
# Mother    = 80
# Boy       = 60
# Girl      = 40
# Bag       = 20
game_players = "F M B G A"

rcs.setPlayers(game_players)
rcs.setdrivers("F M B G")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("F,M F,B F,G F,A M,B M,G")
rcs.setinvalidBank("")
rcs.setboatCapacity(2)

rcs.solve()
