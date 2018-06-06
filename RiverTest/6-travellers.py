import rivercrossingsolver as rcs
from itertools import combinations

game_players = "T1 T2 T3 T1B1 T1B2 T2B1"

no_t1 = []
no_t2 = []
p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]
for y in combos:
    if "T1" not in y and ("T1B1" in y or "T1B2" in y) and (("T2" in y and "T3" not in y) or ("T3" in y and "T2" not in y)):
        no_t1.append(list(y))
    if "T2" not in y and "T2B1" in y and (("T1" in y and "T3" not in y) or ("T3" in y and "T1" not in y)):
        no_t2.append(list(y))

t1_rules = " ".join(x for x in [",".join(x) for x in no_t1])
t2_rules = " ".join(x for x in [",".join(x) for x in no_t2])
final_rules = t1_rules + " " + t2_rules

rcs.setPlayers(game_players)
rcs.setdrivers("T1 T2 T3")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("")
rcs.setinvalidBank(final_rules)
rcs.setboatCapacity(2)

rcs.solve()
