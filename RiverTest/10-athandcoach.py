import rivercrossingsolver as rcs
from itertools import combinations

game_players = "A1 A2 A3 C1 C2 C3"

rule_set = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]
for y in combos:
    if "A1" in y and ("C2" in y or "C3" in y) and "C1" not in y:
        rule_set.append(y)
    if "A2" in y and ("C1" in y or "C3" in y) and "C2" not in y:
        rule_set.append(y)
    if "A3" in y and ("C1" in y or "C2" in y) and "C3" not in y:
        rule_set.append(y)

    # m_count = "".join(y).count("M")
    # c_count = "".join(y).count("C")
    # if len(y) > 2 and m_count > 0 and c_count > m_count:
    #     too_many_criminals.append(list(y))

rules = " ".join(x for x in [",".join(x) for x in rule_set])
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