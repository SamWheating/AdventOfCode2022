with open("input.txt") as ifp:
    strategy = ifp.read().splitlines()


winners = {"A": "Y", "B": "Z", "C": "X"}
ties = {"A": "X", "B": "Y", "C": "Z"}
scores = {"X": 1, "Y": 2, "Z": 3}
score = 0
for game in strategy:
    a, b = game.split(" ")
    if ties[a] == b:
        score += 3
    elif winners[a] == b:
        score += 6
    score += scores[b]

print(f"Solution 1: {score}")

# Part 2

move = {  # Given an instruction (XYZ) and opponents move (ABC), whats the move?
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}
score_for_instruction = {"X": 0, "Y": 3, "Z": 6} # how many points for win/lose/tie
score_for_move = {"X": 1, "Y": 2, "Z": 3} # how many points for r/p/s

score = 0
for game in strategy:
    opponent, instruction = game.split(" ")
    score += score_for_move[move[instruction][opponent]]
    score += score_for_instruction[instruction]

print(f"Solution 2: {score}")
