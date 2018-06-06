import rivercrossingsolver as rcs
from itertools import combinations

# No child with other parents without one own parent
# No child alone
# Only fathers row

game_players = "F1 M1 D1 F2 M2 D2"

rule_set = []
boat_rule_set = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]

for y in combos:
    if "D1" in y and "M1" not in y and "F1" not in y:
        rule_set.append(y)
    if "D2" in y and "M2" not in y and "F2" not in y:
        rule_set.append(y)
    if len(y) == 2:
        if "D1" in y and "F1" not in y:
            boat_rule_set.append(y)
        if "D2" in y and "F2" not in y:
            boat_rule_set.append(y)

rule_set.append(["D1"])
rule_set.append(["D2"])

rules = " ".join(x for x in [",".join(x) for x in rule_set])
boat_rules = " ".join(x for x in [",".join(x) for x in boat_rule_set])

# for r in rule_set:
#     print r
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers("F1 F2")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat(boat_rules)
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()