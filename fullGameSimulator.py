import random



def deck_composition(n):
    game_state = {
        "deck": [0] * 13,
        "cards": 52 * 8,
        "p1": 0,
        "p2": 0,
        "banco": 0
    }
    for i in range(n):
        play(game_state)

def play(gs):
    while gs["cards"]>9:
        deal(gs) 

def deal(gs):
    value = pick(gs) +1
    gs["cards"] -=1
    if value >= 10: value = 0
    
    
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