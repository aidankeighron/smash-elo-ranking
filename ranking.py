import json, os

default_data = {"ELO": 1200, "WINS": 0, "LOSSES": 0, "GAMES": []}
k_factor = 24
def display_stats(data):
    max_length = max(map(len, data.keys()))
    for name, player in data.items():
        print(f"{name+' '*(max_length-len(name))} | ELO: {player['ELO']} | Wins {player['WINS']} | Losses {player['LOSSES']}")
    
def add_score(score, data, file):
    winner, looser, stocks = score.split()
    winning_stocks, loosing_stocks = stocks.split("-")
    stock_difference = int(winning_stocks)-int(loosing_stocks)
    if winner not in data:
        data[winner] = default_data
    if looser not in data:
        data[looser] = default_data
    # Update Wins and Losses
    data[winner]["WINS"] += 1
    data[looser]["LOSSES"] += 1
    # Update Games
    match = {"WINNER": winner, "LOOSER": looser, "STOCKS": stocks}
    data[winner]["GAMES"].append(match)
    data[looser]["GAMES"].append(match)
    # Update Elo
    winner_elo = data[winner]["ELO"]
    looser_elo = data[looser]["ELO"]
    expected = 1/(1+10**((looser_elo-winner_elo)/400))
    data[winner]["ELO"] += k_factor*(stock_difference/6+0.5-expected)
    expected = 1/(1+10**((winner_elo-looser_elo)/400))
    data[looser]["ELO"] += k_factor*(-stock_difference/6+0.5-expected)
    with open(f"{os.path.dirname(__file__)}\\data.json", "w") as file:
        file.write(json.dumps(data))

with open(f"{os.path.dirname(__file__)}\\data.json", "r+") as file:
    try:
        data = json.loads(file.read())
    except Exception:
        data = {"Aidan": default_data}
        file.write(json.dumps(data))

while True:
    print("View Stats (1)\nor add Score (2)")
    choice = input()
    match choice:
        case "1":
            display_stats(data)
        case "2":
            print("Score Formatting 'WINNER_NAME LOOSER_NAME WINNER_STOCKS-LOOSER_STOCKS' EX Aidan Carlos 3-0")
            score = input()
            add_score(score, data, file)
        case _:
            continue