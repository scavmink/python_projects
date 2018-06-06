import rivercrossingsolver as rcs

rcs.setPlayers("F W G C")
rcs.setdrivers("F")
rcs.startLeft()
rcs.setgoalStatus("", "F W G C")
rcs.setinvalidBank("W,G G,C W,G,C")
rcs.setboatCapacity(2)

rcs.solve("farmer")
