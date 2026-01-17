import random
import pandas as pd



def deck_composition(n,nome_strategia):
    report_giocate = []

    game_state = {
        "n":1,
        "deck": [0] * 13,
        "cards": 52 * 8,
        "p1": 0,
        "p2": 0,
        "banco": 0,
        "betValue": 10,
        "balance" : 0,
        "oldBalance" :0,
        "cignoNero" : 0
    }
    for i in range(n):
        game_state["cards"] = 52*8
        game_state["deck"] = [0] *13
        game_state["balance"] = 0
        game_state["cignoNero"] = 0
        play(game_state)
        report_giocate.append({
            "Simulazione": i + 1,
            "Bilancio_Finale": game_state["balance"]
        })

    df = pd.DataFrame(report_giocate)
    nome_file = f"report_metodi/risultati_{nome_strategia}.xlsx"
    df.to_excel(nome_file,index= False)


def play(gs):
    while gs["cards"]>9:
        gs["p1"] = 0
        gs["p2"] = 0
        gs["banco"] = 0
        gs["betValue"] = bet_decider(gs)
        gs["oldBalance"] = gs["balance"]
        deal(gs) 
        #print(gs["n"],") ",end="")
        winners(gs)
        gs["n"] += 1
    print(gs["balance"], end= " ")

def bet_decider(gs):
    if gs["oldBalance"] > gs["balance"]:
        if gs["cignoNero"] >4 : return max(10,gs["betValue"]//2)
        else: return min(80,gs["betValue"]*2)
    elif gs["oldBalance"] == gs["balance"]: return gs["betValue"]
    else: return 10

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

    gs["p1"] = gs["p1"]%10
    gs["p2"] = gs["p2"]%10
    gs["banco"] = gs["banco"]%10
    decision(gs)
    

def decision(gs):
    carte = [0]*2
    if (gs["banco"] < 8):
        if (gs["p1"] <= 4):
            carte[0] = pick(gs) +1
            if carte[0] >= 10: carte[0] = 0
            gs["p1"] += carte[0]
        if gs["p2"]<=4:
            carte[1] = pick(gs) +1
            if carte[1] >= 10: carte[1] = 0
            gs["p2"] += carte[1]
        if gs["banco"]<= 5:
            if banco_playstyle(gs,carte[0],carte[1]) == 1:
                value = pick(gs) +1
                if value >= 10: value = 0
                gs["banco"] += value
    
    gs["p1"] = gs["p1"]%10
    gs["p2"] = gs["p2"]%10
    gs["banco"] = gs["banco"]%10

def pick(gs):
    value = random.randint(0,12)
    while gs["deck"][value]>31:
        value = random.randint(0,12)
    gs["deck"][value] += 1
    gs["cards"] -= 1
    return value

def banco_playstyle(gs,c1,c2):
    if gs["p1"] <= 4 and c1 <= 2 and gs["p2"] <= 4 and c2 <= 2 and gs["banco"] == 4: return 0
    elif gs["p1"] >= 5 and gs["p2"] >= 5 and gs["banco"] == 5: return 1
    elif gs["p1"] >= 8 and gs["p2"] >= 8 and gs["banco"] <= 7: return 1
    elif gs["banco"] <=4: return 1
    else: return 0

def winners(gs):
    # Determiniamo lo stato di p1 rispetto al banco
    res1 = "vince" if gs["p1"] > gs["banco"] else ("come" if gs["p1"] == gs["banco"] else "perde")
    # Determiniamo lo stato di p2 rispetto al banco
    res2 = "vince" if gs["p2"] > gs["banco"] else ("come" if gs["p2"] == gs["banco"] else "perde")
    
    if res1 == "vince": 
        gs["balance"] += gs["betValue"]
        gs["cignoNero"] = 0
    elif res1 == "perde": 
        gs["balance"] -= gs["betValue"]
        gs["cignoNero"] += 1

    #print(f"P1 {res1}, P2 {res2} | Banco aveva: {gs['banco']}")

def main():
    n = int(input("Quante volte vuoi simulare?\n"))
    strategia = "Martingala_parachute"
    deck_composition(n,strategia)

if __name__ == "__main__":
    main()