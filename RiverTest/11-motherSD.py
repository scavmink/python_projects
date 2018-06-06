import rivercrossingsolver as rcs
from itertools import combinations



# Red Mother and Son can row

game_players = "M1 M2 D1 D2 S1 S2"

rule_set = []
brule_set = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]
for y in combos:
    # No child with another mother on bank
    if ("D1" in y or "S1" in y) and "M2" in y and "M1" not in y:
        rule_set.append(y)
    if ("D2" in y or "S2" in y) and "M1" in y and "M2" not in y:
        rule_set.append(y)

# No child on raft with other mother, but other child OK
brule_set = [
    ["M1", "D2"],
    ["M1", "S2"],
    ["M2", "S1"],
    ["M2", "D1"]
]

    # m_count = "".join(y).count("M")
    # c_count = "".join(y).count("C")
    # if len(y) > 2 and m_count > 0 and c_count > m_count:
    #     too_many_criminals.append(list(y))

rules = " ".join(x for x in [",".join(x) for x in rule_set])
brules = " ".join(x for x in [",".join(x) for x in brule_set])

# print rules
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers("M1 S1")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat(brules)
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()