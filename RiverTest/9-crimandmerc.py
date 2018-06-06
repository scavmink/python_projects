import rivercrossingsolver as rcs
from itertools import combinations

game_players = "C1 C2 C3 M1 M2 M3"

too_many_criminals = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]
for y in combos:
    m_count = "".join(y).count("M")
    c_count = "".join(y).count("C")
    if len(y) > 2 and m_count > 0 and c_count > m_count:
        too_many_criminals.append(list(y))

rules = " ".join(x for x in [",".join(x) for x in too_many_criminals])
# print rules
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers("C1 M1")
rcs.setleftBankStatus("C1 C2 C3")
rcs.setrightBankStatus("M1 M2 M3")
rcs.setgoalStatus("M1 M2 M3", "C1 C2 C3")
rcs.setinvalidBoat("")
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()