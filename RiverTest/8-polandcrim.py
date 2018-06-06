import rivercrossingsolver as rcs
from itertools import combinations

game_players = "P1 P2 P3 C1 C2 C3"

too_many_criminals = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]
for y in combos:
    p_count = "".join(y).count("P")
    c_count = "".join(y).count("C")
    if len(y) > 2 and p_count > 0 and c_count > p_count:
        too_many_criminals.append(list(y))

rules = " ".join(x for x in [",".join(x) for x in too_many_criminals])
# print rules
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers(game_players)
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("")
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()