import rivercrossingsolver as rcs
from itertools import combinations

# Two robbers or one robber and one bag
# No robber can be left alone with a bag worth more than what he stole
# Two robbers cannot be left alone with bags that are together worth more than the sum
# of what both originally stole.
#   R1,R2,8 - OK
#   R3,3,5 - OK


game_players = "R1 R2 R3 3 5 8"

rule_set = []
boat_rule_set = []

p = game_players.split()
combos = [x for l in range(1,len(game_players)) for x in combinations(p,l)]

# for y in combos:
rule_set = [
('R1', '5'),
('R1', '8'),
('R2', '8'),
('R1', '3', '5'),
('R1', '3', '8'),
('R1', '5', '8'),
('R2', '3', '5'),
('R2', '3', '8'),
('R2', '5', '8'),
('R3', '3', '8'),
('R3', '5', '8'),
('R1', 'R2', '3', '8'),
('R1', 'R2', '5', '8'),
('R1', 'R3', '5', '8'),
('R1', '3', '5', '8'),
('R2', '3', '5', '8'),
('R3', '3', '5', '8'),
('R1', 'R2', '3', '5', '8'),
('R1', 'R3', '3', '5', '8'),
('R2', 'R3', '3', '5', '8')
]

rules = " ".join(x for x in [",".join(x) for x in rule_set])
# boat_rules = " ".join(x for x in [",".join(x) for x in boat_rule_set])

# for r in rule_set:
#     print r
# exit(0)


rcs.setPlayers(game_players)
rcs.setdrivers("R1 R2 R3")
rcs.startLeft()
rcs.setgoalStatus("", game_players)
rcs.setinvalidBoat("")
rcs.setinvalidBank(rules)
rcs.setboatCapacity(2)

rcs.solve()