import rivercrossingsolver as rcs
from itertools import combinations

# No farmer, dog bites everyone
# No boy, girl teases rabbits
# No girl, boy teases squirrels
# All people can row
# Two people or one person and one animal

game_players = "F S D DOG SQ1 SQ2 R1 R2"

rule_set = []
boat_rule_set = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]

for y in combos:
    if "F" not in y and "DOG" in y and len(y) > 1:
        rule_set.append(y)
    if "S" not in y and "D" in y and ("R1" in y or "R2" in y):
        rule_set.append(y)
    if "D" not in y and "S" in y and ("SQ1" in y or "SQ2" in y):
        rule_set.append(y)

rules = " ".join(x for x in [",".join(x) for x in rule_set])
# boat_rules = " ".join(x for x in [",".join(x) for x in boat_rule_set])

# for r in rule_set:
#     print r
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers("F S D")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("")
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()