import random



def deck_composition(n):
    game_state = {
        #"n":1,
        "deck": [0] * 13,
        "cards": 52 * 8,
        "p1": 0,
        "p2": 0,
        "banco": 0
    }
    for i in range(n):
        game_state["cards"] = 52*8
        game_state["deck"] = [0] *13
        play(game_state)

def play(gs):
    while gs["cards"]>9:
        gs["p1"] = 0
        gs["p2"] = 0
        gs["banco"] = 0
        deal(gs) 

def deal(gs):
    for i in range(2):
        value = pick(gs) +1
        if value >= 10: value = 0
        gs["p1"] += value

        value = pick(gs) +1
        if value >= 10: value = 0
        gs["p2"] += value

        value = pick(gs) +1
        if value >= 10: value = 0
        gs["banco"] += value

        gs["cards"] -=3

    gs["p1"] = gs["p1"]%10
    gs["p2"] = gs["p2"]%10
    gs["banco"] = gs["banco"]%10
    #print(gs)
    #gs["n"] += 1
    
    
def pick(gs):
    value = random.randint(0,12)
    while gs["deck"][value]>31:
        value = random.randint(0,12)
    gs["deck"][value] += 1
    return value
    
def main():
    n = int(input("Quante volte vuoi simulare?\n"))
    deck_composition(n)

if __name__ == "__main__":
    main()